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
        parent=None,
    ):
        super().__init__(parent)
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
        )
        env = KissKHWrapper.get_environment(
            stream_key=self.stream_key,
            sub_key=self.sub_key,
            decrypt_key=self.decrypt_key,
            decrypt_iv=self.decrypt_iv,
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
                env=env,
                bufsize=1,
                creationflags=creationflags,
            )

            current_percent = 0
            speed_text = ""
            status_text = "Downloading..."

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

    def __init__(self, episode_url: str, parent=None):
        super().__init__(parent)
        self.episode_url = episode_url

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

