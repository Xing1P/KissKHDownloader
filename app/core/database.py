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
