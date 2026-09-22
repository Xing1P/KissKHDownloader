import json
import sqlite3
import os
import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Manages SQLite database storage for KissKH download history."""

    def __init__(self, db_path: str = "history.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates history table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS download_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT,
                    title TEXT NOT NULL,
                    episodes TEXT,
                    quality TEXT,
                    subtitle_lang TEXT,
                    output_dir TEXT,
                    status TEXT,
                    completed_at TEXT
                )
            """)
            # Per-episode download tasks; failed/unfinished rows are restored on next launch.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS download_tasks (
                    task_id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    drama_title TEXT,
                    drama_url TEXT,
                    episode INTEGER,
                    params TEXT,
                    status TEXT,
                    attempts INTEGER DEFAULT 0,
                    error TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    def add_record(
        self,
        task_id: str,
        title: str,
        episodes: str,
        quality: str,
        subtitle_lang: str,
        output_dir: str,
        status: str = "Completed",
    ) -> int:
        """Inserts a new download record into the history database."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO download_history (
                    task_id, title, episodes, quality, subtitle_lang, output_dir, status, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, title, episodes, quality, subtitle_lang, output_dir, status, timestamp))
            conn.commit()
            return cursor.lastrowid

    def get_all_records(self, search_query: str = "") -> List[Dict[str, Any]]:
        """Retrieves download history records with optional search filter."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if search_query:
                cursor.execute("""
                    SELECT * FROM download_history
                    WHERE title LIKE ? OR episodes LIKE ? OR status LIKE ?
                    ORDER BY id DESC
                """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
            else:
                cursor.execute("SELECT * FROM download_history ORDER BY id DESC")

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def delete_records_by_task_id(self, task_id: str):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM download_history WHERE task_id = ?", (task_id,))
            conn.commit()

    def delete_record(self, record_id: int):
        """Deletes a record by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM download_history WHERE id = ?", (record_id,))
            conn.commit()

    def clear_all_records(self):
        """Clears all records from history table."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM download_history")
            conn.commit()

    # --- Episode download tasks ---

    @staticmethod
    def _now() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def upsert_task(self, task: Dict[str, Any]):
        """Inserts or replaces an episode task."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO download_tasks (
                    task_id, group_id, drama_title, drama_url, episode, params, status, attempts, error, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task["task_id"], task["group_id"], task["drama_title"], task["drama_url"],
                task["episode"], json.dumps(task["params"]), task["status"],
                task.get("attempts", 0), task.get("error", ""), self._now(),
            ))
            conn.commit()

    def update_task_status(self, task_id: str, status: str, attempts: int, error: str = ""):
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE download_tasks SET status = ?, attempts = ?, error = ?, updated_at = ? WHERE task_id = ?",
                (status, attempts, error, self._now(), task_id),
            )
            conn.commit()

    def get_restorable_tasks(self) -> List[Dict[str, Any]]:
        """Returns all tasks of movies that still have unfinished episodes.

        Episodes cut off mid-download are marked failed ("Interrupted"); movies whose
        episodes all completed are dropped.
        """
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE download_tasks SET status = 'failed', error = 'Interrupted' WHERE status = 'downloading'"
            )
            conn.execute("""
                DELETE FROM download_tasks WHERE group_id NOT IN (
                    SELECT group_id FROM download_tasks WHERE status != 'completed'
                )
            """)
            conn.commit()
            rows = conn.execute("SELECT * FROM download_tasks ORDER BY rowid").fetchall()
        tasks = []
        for row in rows:
            task = dict(row)
            task["params"] = json.loads(task["params"] or "{}")
            tasks.append(task)
        return tasks

    def delete_tasks(self, task_ids: List[str]):
        if not task_ids:
            return
        with self._get_connection() as conn:
            conn.executemany("DELETE FROM download_tasks WHERE task_id = ?", [(t,) for t in task_ids])
            conn.commit()

    def delete_completed_tasks(self):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM download_tasks WHERE status = 'completed'")
            conn.commit()
