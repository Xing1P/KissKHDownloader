import os
from pathlib import Path
from PySide6.QtCore import QSettings

class AppConfig:
    """Manages application settings persistence using QSettings."""
    
    ORGANIZATION = "KissKH"
    APPLICATION = "KissKHDownloaderQt"

    def __init__(self):
        self.settings = QSettings(self.ORGANIZATION, self.APPLICATION)

    @property
    def default_output_dir(self) -> str:
        fallback_path = str(Path.home() / "Downloads" / "KissKH_Downloads")
        path = self.settings.value("output_dir", "", type=str) or fallback_path
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            # Saved drive/folder is unavailable (e.g. removed disk) - fall back safely.
            path = fallback_path
            os.makedirs(path, exist_ok=True)
        return path

    @default_output_dir.setter
    def default_output_dir(self, value: str):
        self.settings.setValue("output_dir", value)

    @property
    def default_quality(self) -> str:
        return self.settings.value("default_quality", "1080p", type=str)

    @default_quality.setter
    def default_quality(self, value: str):
        self.settings.setValue("default_quality", value)

    @property
    def enable_subtitles(self) -> bool:
        return self.settings.value("enable_subtitles", True, type=bool)

    @enable_subtitles.setter
    def enable_subtitles(self, value: bool):
        self.settings.setValue("enable_subtitles", value)

    @property
    def decrypt_subtitles(self) -> bool:
        return self.settings.value("decrypt_subtitles", False, type=bool)

    @decrypt_subtitles.setter
    def decrypt_subtitles(self, value: bool):
        self.settings.setValue("decrypt_subtitles", value)

    @property
    def decrypt_key(self) -> str:
        return self.settings.value("decrypt_key", "", type=str)

    @decrypt_key.setter
    def decrypt_key(self, value: str):
        self.settings.setValue("decrypt_key", value)

    @property
    def decrypt_iv(self) -> str:
        return self.settings.value("decrypt_iv", "", type=str)

    @decrypt_iv.setter
    def decrypt_iv(self, value: str):
        self.settings.setValue("decrypt_iv", value)


    @property
    def subtitle_language(self) -> str:
        return self.settings.value("subtitle_language", "en", type=str)

    @subtitle_language.setter
    def subtitle_language(self, value: str):
        self.settings.setValue("subtitle_language", value)

    @property
    def stream_key(self) -> str:
        return self.settings.value("stream_key", "", type=str)

    @stream_key.setter
    def stream_key(self, value: str):
        self.settings.setValue("stream_key", value)

    @property
    def sub_key(self) -> str:
        return self.settings.value("sub_key", "", type=str)

    @sub_key.setter
    def sub_key(self, value: str):
        self.settings.setValue("sub_key", value)

    @property
    def max_concurrent_downloads(self) -> int:
        return self.settings.value("max_concurrent_downloads", 1, type=int)

    @max_concurrent_downloads.setter
    def max_concurrent_downloads(self, value: int):
        self.settings.setValue("max_concurrent_downloads", value)

    @property
    def website_url(self) -> str:
        return self.settings.value("website_url", "https://kisskh.is/", type=str)

    @website_url.setter
    def website_url(self, value: str):
        self.settings.setValue("website_url", value)

    @property
    def theme(self) -> str:
        return self.settings.value("theme", "dark", type=str)

    @theme.setter
    def theme(self, value: str):
        self.settings.setValue("theme", value)

    @property
    def language(self) -> str:
        return self.settings.value("language", "en", type=str)

    @language.setter
    def language(self, value: str):
        self.settings.setValue("language", value)


