import uuid
from typing import Dict, List, Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QLabel, QStatusBar, QSplitter, QPushButton, QFrame, QButtonGroup
)
import os
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from app.__version__ import __version__, __app_name__
from app.core.config import AppConfig
from app.core.database import DatabaseManager
from app.core.i18n import tr
from app.core.worker import DownloadWorker
from app.ui.downloader_tab import DownloaderTab
from app.ui.queue_tab import QueueTab
from app.ui.settings_tab import SettingsTab
from app.ui.history_tab import HistoryTab
from app.ui.web_tab import WebTab
from app.ui.log_widget import LogWidget
from app.ui.styles import get_theme_qss



class MainWindow(QMainWindow):
    """Main Application Window with Left Sidebar Navigation."""

    def __init__(self):
        super().__init__()
        self.config = AppConfig()
        self.db = DatabaseManager()
        self.download_queue: List[dict] = []
        self.active_workers: Dict[str, DownloadWorker] = {}
        self.active_worker_data: Dict[str, dict] = {}
        self.current_running_task_id: Optional[str] = None

        self.setWindowTitle(f"{__app_name__} v{__version__} (Qt6)")
        self.setMinimumSize(1100, 720)

        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()
        self.apply_theme()
        self.retranslate_ui()


    def apply_theme(self):
        theme_qss = get_theme_qss(self.config.theme)
        self.setStyleSheet(theme_qss)
        if hasattr(self, "theme_toggle_btn"):
            if self.config.theme == "light":
                self.theme_toggle_btn.setText("☀️  Light Mode (ភ្លឺ)")
            else:
                self.theme_toggle_btn.setText("🌙  Dark Mode (ងងឹត)")

    def toggle_theme(self):
        new_theme = "light" if self.config.theme == "dark" else "dark"
        self.config.theme = new_theme
        self.apply_theme()
        if hasattr(self, "settings_tab"):
            idx = self.settings_tab.theme_combo.findData(new_theme)
            if idx >= 0:
                self.settings_tab.theme_combo.setCurrentIndex(idx)

    def toggle_language(self):
        new_lang = "km" if self.config.language == "en" else "en"
        self.config.language = new_lang
        self.retranslate_ui()
        if hasattr(self, "settings_tab"):
            idx = self.settings_tab.lang_combo.findData(new_lang)
            if idx >= 0:
                self.settings_tab.lang_combo.setCurrentIndex(idx)

    def retranslate_ui(self):
        lang = self.config.language
        self.btn_web.setText(f"  {tr('nav_browse', lang)}")
        self.btn_downloader.setText(f"  {tr('nav_downloader', lang)}")
        self.update_queue_tab_title()
        self.btn_history.setText(f"  {tr('nav_history', lang)}")
        self.btn_settings.setText(f"  {tr('nav_settings', lang)}")
        self.title_label.setText(tr("app_title", lang))
        self.subtitle_label.setText(f"v{__version__} • {tr('app_subtitle', lang)}")



        if hasattr(self, "lang_toggle_btn"):
            self.lang_toggle_btn.setText("🇰🇭  ភាសាខ្មែរ (Khmer)" if lang == "km" else "🇬🇧  English")


        # Retranslate all child tabs
        if hasattr(self, "web_tab"):
            self.web_tab.retranslate_ui()
        if hasattr(self, "downloader_tab"):
            self.downloader_tab.retranslate_ui()
        if hasattr(self, "queue_tab"):
            self.queue_tab.retranslate_ui()
        if hasattr(self, "history_tab"):
            self.history_tab.retranslate_ui()
        if hasattr(self, "settings_tab"):
            self.settings_tab.retranslate_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -------------------------------------------------------------
        # Left Navigation Sidebar (Width: 230px)
        # -------------------------------------------------------------
        sidebar = QFrame()
        sidebar.setProperty("class", "sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 16, 14, 16)
        sidebar_layout.setSpacing(8)

        # App Brand Header in Sidebar
        brand_box = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setProperty("class", "brand-title")
        self.subtitle_label = QLabel()
        self.subtitle_label.setProperty("class", "brand-subtitle")

        brand_box.addWidget(self.title_label)
        brand_box.addWidget(self.subtitle_label)
        sidebar_layout.addLayout(brand_box)

        sidebar_layout.addSpacing(16)

        # Navigation Buttons Group
        self.nav_bg = QButtonGroup(self)
        self.nav_bg.setExclusive(True)

        icons_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icons"))

        self.btn_web = QPushButton()
        self.btn_web.setCheckable(True)
        self.btn_web.setChecked(True)
        self.btn_web.setProperty("class", "nav-btn")
        self.btn_web.setIcon(QIcon(os.path.join(icons_dir, "browse.png")))
        self.btn_web.setIconSize(QSize(24, 24))
        self.nav_bg.addButton(self.btn_web, 0)
        sidebar_layout.addWidget(self.btn_web)

        self.btn_downloader = QPushButton()
        self.btn_downloader.setCheckable(True)
        self.btn_downloader.setProperty("class", "nav-btn")
        self.btn_downloader.setIcon(QIcon(os.path.join(icons_dir, "download.png")))
        self.btn_downloader.setIconSize(QSize(24, 24))
        self.nav_bg.addButton(self.btn_downloader, 1)
        sidebar_layout.addWidget(self.btn_downloader)

        self.btn_queue = QPushButton()
        self.btn_queue.setCheckable(True)
        self.btn_queue.setProperty("class", "nav-btn")
        self.btn_queue.setIcon(QIcon(os.path.join(icons_dir, "queue.png")))
        self.btn_queue.setIconSize(QSize(24, 24))
        self.nav_bg.addButton(self.btn_queue, 2)
        sidebar_layout.addWidget(self.btn_queue)

        self.btn_history = QPushButton()
        self.btn_history.setCheckable(True)
        self.btn_history.setProperty("class", "nav-btn")
        self.btn_history.setIcon(QIcon(os.path.join(icons_dir, "history.png")))
        self.btn_history.setIconSize(QSize(24, 24))
        self.nav_bg.addButton(self.btn_history, 3)
        sidebar_layout.addWidget(self.btn_history)

        self.btn_settings = QPushButton()
        self.btn_settings.setCheckable(True)
        self.btn_settings.setProperty("class", "nav-btn")
        self.btn_settings.setIcon(QIcon(os.path.join(icons_dir, "settings.png")))
        self.btn_settings.setIconSize(QSize(24, 24))
        self.nav_bg.addButton(self.btn_settings, 4)
        sidebar_layout.addWidget(self.btn_settings)


        self.nav_bg.idClicked.connect(self.on_nav_button_clicked)

        sidebar_layout.addStretch()

        # Quick Toggles (Theme & Language - Vertical Layout)
        toggle_box = QVBoxLayout()
        toggle_box.setSpacing(6)

        self.theme_toggle_btn = QPushButton("🌙  Dark Mode")
        self.theme_toggle_btn.setFixedHeight(34)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        toggle_box.addWidget(self.theme_toggle_btn)

        self.lang_toggle_btn = QPushButton("🇬🇧  English")
        self.lang_toggle_btn.setFixedHeight(34)
        self.lang_toggle_btn.clicked.connect(self.toggle_language)
        toggle_box.addWidget(self.lang_toggle_btn)

        sidebar_layout.addLayout(toggle_box)


        # Sidebar Active Badge Indicator
        self.active_count_badge = QLabel("Active Downloads: 0")
        self.active_count_badge.setProperty("class", "badge-card")
        sidebar_layout.addWidget(self.active_count_badge)


        root_layout.addWidget(sidebar)

        # -------------------------------------------------------------
        # Main Content Area (Splitter: StackedWidget top, LogWidget bottom)
        # -------------------------------------------------------------
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        splitter = QSplitter(Qt.Vertical)

        # Stacked Widget for Main Views
        self.stacked_widget = QStackedWidget()

        # View 0: Embedded Browser
        self.web_tab = WebTab(self.config)
        self.web_tab.send_to_downloader.connect(self.on_url_captured_from_browser)
        self.stacked_widget.addWidget(self.web_tab)

        # View 1: New Download Form
        self.downloader_tab = DownloaderTab(self.config)
        self.downloader_tab.download_requested.connect(self.start_download_immediately)
        self.downloader_tab.add_queue_requested.connect(self.add_to_queue)
        self.stacked_widget.addWidget(self.downloader_tab)

        # View 2: Download Queue
        self.queue_tab = QueueTab(self.config)
        self.queue_tab.start_queue_requested.connect(self.process_queue)
        self.queue_tab.clear_completed_requested.connect(self.clear_completed_queue)
        self.stacked_widget.addWidget(self.queue_tab)

        # View 3: Download History (SQLite)
        self.history_tab = HistoryTab(self.db, self.config)
        self.history_tab.redownload_requested.connect(self.on_redownload_from_history)
        self.stacked_widget.addWidget(self.history_tab)

        # View 4: Settings & Keys
        self.settings_tab = SettingsTab(self.config)
        self.settings_tab.log_signal.connect(self.on_log_message)
        self.settings_tab.settings_saved.connect(self.on_settings_saved)
        self.stacked_widget.addWidget(self.settings_tab)

        splitter.addWidget(self.stacked_widget)

        # Activity Log Console Widget
        self.log_widget = LogWidget()
        splitter.addWidget(self.log_widget)

        # Allocate 85%+ vertical height to StackedWidget
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([850, 110])

        content_layout.addWidget(splitter, 1)

        root_layout.addWidget(content_container, 1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        self.log_widget.log("INFO", "KissKH Downloader Qt6 application started successfully.")

    def on_nav_button_clicked(self, index: int):
        self.stacked_widget.setCurrentIndex(index)

    def switch_page(self, index: int):
        btn = self.nav_bg.button(index)
        if btn:
            btn.setChecked(True)
        self.stacked_widget.setCurrentIndex(index)

    def update_queue_tab_title(self):
        count = len(self.download_queue) + len(self.active_workers)
        lang = self.config.language
        self.btn_queue.setText(f"  {tr('nav_queue', lang, count=count)}")
        self.active_count_badge.setText(tr("active_downloads", lang, count=len(self.active_workers)))


    def on_url_captured_from_browser(self, url: str):
        self.downloader_tab.url_input.setText(url)
        self.switch_page(1)
        self.log_widget.log("INFO", f"Captured URL from browser: {url}")
        self.status_bar.showMessage("URL loaded into downloader!", 4000)

    def on_redownload_from_history(self, rec: dict):
        title = rec.get("title", "")
        self.downloader_tab.url_input.setText(title)
        self.switch_page(1)
        self.log_widget.log("INFO", f"Loaded title from history: {title}")
        self.status_bar.showMessage("Loaded from history ready for download!", 4000)

    def on_settings_saved(self):
        self.apply_theme()
        self.retranslate_ui()
        self.web_tab.navigate_home()
        self.log_widget.log("INFO", "Settings saved. Updated theme, language, and reloaded home URL.")

    def start_download_immediately(self, data: dict):
        if not data.get("url_or_name"):
            self.log_widget.log("WARNING", "Please enter a valid KissKH URL or movie title.")
            self.status_bar.showMessage("Error: URL or title is required", 4000)
            return

        task_id = str(uuid.uuid4())[:8]
        self.queue_tab.add_queue_item(task_id, data)
        self.switch_page(2)
        self.log_widget.log("INFO", f"Queued download for: {data.get('url_or_name')}")
        
        self.download_queue.append({"task_id": task_id, "data": data})
        self.update_queue_tab_title()
        self.process_queue()

    def add_to_queue(self, data: dict):
        if not data.get("url_or_name"):
            self.log_widget.log("WARNING", "Please enter a valid KissKH URL or movie title.")
            return

        task_id = str(uuid.uuid4())[:8]
        self.queue_tab.add_queue_item(task_id, data)
        self.download_queue.append({"task_id": task_id, "data": data})
        self.update_queue_tab_title()
        self.log_widget.log("INFO", f"Added item to download queue (Task ID: {task_id})")
        self.status_bar.showMessage("Added to queue", 3000)

    def process_queue(self):
        if self.current_running_task_id or not self.download_queue:
            return

        next_item = self.download_queue.pop(0)
        task_id = next_item["task_id"]
        data = next_item["data"]

        worker = DownloadWorker(
            task_id=task_id,
            url_or_name=data["url_or_name"],
            output_dir=data["output_dir"],
            quality=data["quality"],
            first_ep=data["first_ep"],
            last_ep=data["last_ep"],
            all_episodes=data["all_episodes"],
            enable_subtitles=data["enable_subtitles"],
            sub_lang=data["sub_lang"],
            decrypt_subtitles=data["decrypt_subtitles"],
            stream_key=self.config.stream_key,
            sub_key=self.config.sub_key,
            decrypt_key=self.config.decrypt_key,
            decrypt_iv=self.config.decrypt_iv,
        )

        worker.progress_signal.connect(self.on_worker_progress)
        worker.log_signal.connect(self.on_worker_log)
        worker.finished_signal.connect(self.on_worker_finished)

        self.active_workers[task_id] = worker
        self.active_worker_data[task_id] = data
        self.current_running_task_id = task_id
        self.update_queue_tab_title()

        self.status_bar.showMessage(f"Downloading task {task_id}...")
        worker.start()

    def on_worker_progress(self, task_id: str, percent: int, speed: str, status: str):
        self.queue_tab.update_task_progress(task_id, percent, speed, status)
        self.status_bar.showMessage(f"Task {task_id}: {status} ({speed})")

    def on_worker_log(self, task_id: str, level: str, message: str):
        self.log_widget.log(level, f"[{task_id}] {message}")

    def on_worker_finished(self, task_id: str, success: bool, message: str):
        data = self.active_worker_data.pop(task_id, {})
        if task_id in self.active_workers:
            del self.active_workers[task_id]

        self.current_running_task_id = None
        status_text = "Completed" if success else f"Failed ({message})"
        self.queue_tab.update_task_status(task_id, status_text)
        self.update_queue_tab_title()

        episodes_str = "All"
        if data and not data.get("all_episodes"):
            episodes_str = f"Ep {data.get('first_ep')}-{data.get('last_ep')}"

        self.db.add_record(
            task_id=task_id,
            title=data.get("url_or_name", "Unknown Title"),
            episodes=episodes_str,
            quality=data.get("quality", "1080p"),
            subtitle_lang=data.get("sub_lang", "en"),
            output_dir=data.get("output_dir", ""),
            status=status_text,
        )

        self.status_bar.showMessage(f"Task {task_id} finished: {message}", 5000)
        self.process_queue()

    def on_log_message(self, level: str, message: str):
        self.log_widget.log(level, message)

    def clear_completed_queue(self):
        self.queue_tab.remove_completed_items()
        self.update_queue_tab_title()
