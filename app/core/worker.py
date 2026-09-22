import subprocess
import re
import os
import sys
from typing import Optional, List
from PySide6.QtCore import QThread, Signal
from app.core.kisskh_wrapper import KissKHWrapper

class DownloadWorker(QThread):
    """Background worker thread for running kisskh-downloader downloads."""
    
    # task_id, percentage, speed, status_text
    progress_signal = Signal(str, int, str, str)
    # task_id, log_level (INFO/WARNING/ERROR/SUCCESS), message
    log_signal = Signal(str, str, str)
    # task_id, success, message
    finished_signal = Signal(str, bool, str)

    def __init__(
        self,
        task_id: str,
        url_or_name: str,
        output_dir: str,
        quality: str = "1080p",
        first_ep: Optional[int] = None,
        last_ep: Optional[int] = None,
        all_episodes: bool = True,
        enable_subtitles: bool = True,
        sub_lang: str = "en",
        decrypt_subtitles: bool = False,
        stream_key: str = "",
        sub_key: str = "",
        decrypt_key: str = "",
        decrypt_iv: str = "",
        base_url: str = "",
        skip_recap: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.base_url = base_url
        self.skip_recap = skip_recap
        self.task_id = task_id
        self.url_or_name = url_or_name
        self.output_dir = output_dir
        self.quality = quality
        self.first_ep = first_ep
        self.last_ep = last_ep
        self.all_episodes = all_episodes
        self.enable_subtitles = enable_subtitles
        self.sub_lang = sub_lang
        self.decrypt_subtitles = decrypt_subtitles
        self.stream_key = stream_key
        self.sub_key = sub_key
        self.decrypt_key = decrypt_key
        self.decrypt_iv = decrypt_iv

        self.process: Optional[subprocess.Popen] = None
        self._is_cancelled = False

    def cancel(self):
        """Cancels the running process."""
        self._is_cancelled = True
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
            except Exception:
                pass

    def run(self):
        cmd = KissKHWrapper.build_download_cmd(
            url_or_name=self.url_or_name,
            output_dir=self.output_dir,
            quality=self.quality,
            first_ep=self.first_ep,
            last_ep=self.last_ep,
            all_episodes=self.all_episodes,
            enable_subtitles=self.enable_subtitles,
            sub_lang=self.sub_lang,
            decrypt_subtitles=self.decrypt_subtitles,
            decrypt_key=self.decrypt_key,
            decrypt_iv=self.decrypt_iv,
            skip_recap=self.skip_recap,
        )
        env = KissKHWrapper.get_environment(
            stream_key=self.stream_key,
            sub_key=self.sub_key,
            decrypt_key=self.decrypt_key,
            decrypt_iv=self.decrypt_iv,
            base_url=self.base_url,
        )


        self.log_signal.emit(self.task_id, "INFO", f"Starting command: {' '.join(cmd)}")
        self.progress_signal.emit(self.task_id, 0, "-- KB/s", "Starting download...")

        try:
            # On Windows hide console window for subprocess
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                bufsize=1,
                creationflags=creationflags,
            )

            current_percent = 0
            speed_text = ""
            status_text = "Downloading..."
            # The CLI logs some per-episode failures and still exits 0.
            soft_error = ""

            while True:
                if self._is_cancelled:
                    self.log_signal.emit(self.task_id, "WARNING", "Download cancelled by user.")
                    self.finished_signal.emit(self.task_id, False, "Cancelled")
                    return

                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break

                if line:
                    clean_line = line.strip()
                    if clean_line:
                        lower_line = clean_line.lower()
                        if "failed to generate authentication token" in lower_line:
                            soft_error = "Failed to generate authentication token"
                        elif "still not released" in lower_line:
                            soft_error = "Episode not released yet"
                        # Log output line
                        if "error" in clean_line.lower() or "exception" in clean_line.lower():
                            self.log_signal.emit(self.task_id, "ERROR", clean_line)
                        elif "warning" in clean_line.lower():
                            self.log_signal.emit(self.task_id, "WARNING", clean_line)
                        elif "download" in clean_line.lower() or "completed" in clean_line.lower():
                            self.log_signal.emit(self.task_id, "SUCCESS", clean_line)
                        else:
                            self.log_signal.emit(self.task_id, "INFO", clean_line)

                        # Regex parsing progress percentage
                        percent_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", clean_line)
                        if percent_match:
                            try:
                                current_percent = int(float(percent_match.group(1)))
                            except ValueError:
                                pass

                        # Speed parsing
                        speed_match = re.search(r"(\d+(?:\.\d+)?\s*(?:KiB|MiB|GiB|B|KB|MB)/s)", clean_line, re.IGNORECASE)
                        if speed_match:
                            speed_text = speed_match.group(1)

                        # Episode info parsing
                        ep_match = re.search(r"(?:Episode|Ep)\s*(\d+)", clean_line, re.IGNORECASE)
                        if ep_match:
                            status_text = f"Downloading Episode {ep_match.group(1)}"

                        self.progress_signal.emit(self.task_id, current_percent, speed_text, status_text)

            rc = self.process.poll()
            if self._is_cancelled:
                self.finished_signal.emit(self.task_id, False, "Cancelled")
            elif rc == 0 and soft_error:
                self.log_signal.emit(self.task_id, "ERROR", soft_error)
                self.finished_signal.emit(self.task_id, False, soft_error)
            elif rc == 0:
                self.progress_signal.emit(self.task_id, 100, "Done", "Completed successfully")
                self.log_signal.emit(self.task_id, "SUCCESS", "Download finished successfully!")
                self.finished_signal.emit(self.task_id, True, "Completed")
            else:
                self.log_signal.emit(self.task_id, "ERROR", f"Process exited with error code {rc}")
                self.finished_signal.emit(self.task_id, False, f"Failed with exit code {rc}")

        except Exception as e:
            self.log_signal.emit(self.task_id, "ERROR", f"Execution error: {str(e)}")
            self.finished_signal.emit(self.task_id, False, str(e))


class PlaywrightInstallWorker(QThread):
    """Background worker for installing Playwright Chromium browser."""

    log_signal = Signal(str, str) # level, message
    finished_signal = Signal(bool, str) # success, message

    def run(self):
        cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
        self.log_signal.emit("INFO", f"Running: {' '.join(cmd)}")
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=creationflags,
            )
            for line in process.stdout:
                if line.strip():
                    self.log_signal.emit("INFO", line.strip())

            process.wait()
            if process.returncode == 0:
                self.finished_signal.emit(True, "Playwright Chromium installed successfully!")
            else:
                self.finished_signal.emit(False, f"Installation failed with code {process.returncode}")
        except Exception as e:
            self.finished_signal.emit(False, f"Failed to run installer: {str(e)}")


class GetKeyWorker(QThread):
    """Background worker for executing kisskh get-key <URL>."""

    log_signal = Signal(str, str) # level, message
    # success, stream_key, sub_key, message
    finished_signal = Signal(bool, str, str, str)

    def __init__(self, episode_url: str, base_url: str = "", parent=None):
        super().__init__(parent)
        self.episode_url = episode_url
        self.base_url = base_url

    def run(self):
        cmd = [sys.executable, "-m", "kisskh_downloader.cli", "get-key", self.episode_url]
        self.log_signal.emit("INFO", f"Extracting keys using command: {' '.join(cmd)}")
        try:
            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=KissKHWrapper.get_environment(base_url=self.base_url),
                creationflags=creationflags,
            )
            stream_key = ""
            sub_key = ""
            for line in process.stdout:
                clean = line.strip()
                if clean:
                    self.log_signal.emit("INFO", clean)
                    if "KISSKH_STREAM_KEY=" in clean or "stream_key=" in clean.lower():
                        parts = clean.split("=")
                        if len(parts) > 1:
                            stream_key = parts[1].strip().strip('"').strip("'")
                    if "KISSKH_SUB_KEY=" in clean or "sub_key=" in clean.lower():
                        parts = clean.split("=")
                        if len(parts) > 1:
                            sub_key = parts[1].strip().strip('"').strip("'")

            process.wait()
            if process.returncode == 0:
                self.finished_signal.emit(True, stream_key, sub_key, "Keys extracted successfully!")
            else:
                self.finished_signal.emit(False, "", "", f"Failed to extract keys (Code {process.returncode})")
        except Exception as e:
            self.finished_signal.emit(False, "", "", f"Error: {str(e)}")



class ResolveEpisodesWorker(QThread):
    """Looks up a drama's episode numbers so each episode can be downloaded as its own task."""

    # group_id, drama_title, drama_url, episode numbers
    resolved_signal = Signal(str, str, str, list)
    # group_id, error message
    failed_signal = Signal(str, str)

    def __init__(
        self,
        group_id: str,
        url_or_name: str,
        base_url: str,
        first_ep: Optional[int] = None,
        last_ep: Optional[int] = None,
        all_episodes: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self.group_id = group_id
        self.url_or_name = url_or_name.strip()
        self.base_url = base_url
        self.first_ep = first_ep
        self.last_ep = last_ep
        self.all_episodes = all_episodes

    def run(self):
        try:
            from urllib.parse import urlsplit, parse_qs, unquote
            from kisskh_downloader.kisskh_api import KissKHApi

            parts = urlsplit(self.base_url.strip())
            site = f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else None
            api = KissKHApi(base_url=site)

            single_episode: Optional[int] = None
            if self.url_or_name.lower().startswith(("http://", "https://")):
                url_parts = urlsplit(self.url_or_name)
                ids = parse_qs(url_parts.query).get("id")
                if not ids:
                    raise ValueError("Not a valid drama URL (missing ?id=...).")
                drama_id = int(ids[0])
                segments = url_parts.path.split("/")
                slug = segments[2] if len(segments) > 2 else "Drama"
                title = unquote(slug).replace("-", " ").replace("_", " ")
                drama_url = KissKHWrapper.drama_url(self.url_or_name)
                # An episode URL on its own means "just this episode", matching the CLI.
                ep_match = re.search(r"Episode-(\d+)", url_parts.path)
                if self.all_episodes and ep_match and parse_qs(url_parts.query).get("ep"):
                    single_episode = int(ep_match.group(1))
            else:
                results = list(api.search_dramas_by_query(self.url_or_name))
                if not results:
                    raise ValueError(f"No drama found for '{self.url_or_name}'.")
                query = self.url_or_name.lower()
                drama = next((d for d in results if d.title.lower() == query), results[0])
                drama_id = drama.id
                title = drama.title
                drama_url = f"{api.site_domain}/Drama/{drama.title.replace(' ', '-')}?id={drama.id}"

            if single_episode is not None:
                start = stop = single_episode
            elif self.all_episodes:
                start, stop = 1, sys.maxsize
            else:
                start = self.first_ep or 1
                stop = self.last_ep or sys.maxsize

            episode_ids = api.get_episode_ids(drama_id=drama_id, start=start, stop=stop, skip_recap=True)
            episodes = sorted(int(num) for num in episode_ids)
            if not episodes:
                raise ValueError("No episodes found in the selected range.")
            self.resolved_signal.emit(self.group_id, title, drama_url, episodes)
        except Exception as e:
            self.failed_signal.emit(self.group_id, f"Could not load episode list: {e}")
