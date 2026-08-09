from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QSizePolicy
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Signal
from app.core.config import AppConfig
from app.core.i18n import tr

class WebTab(QWidget):
    """Embedded Web Browser Tab for KissKH Website with URL capture."""

    send_to_downloader = Signal(str) # Emits active page URL

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Toolbar Card
        nav_card = QFrame()
        nav_card.setProperty("class", "card")
        nav_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_card)
        nav_layout.setContentsMargins(8, 4, 8, 4)
        nav_layout.setSpacing(6)

        # Back
        self.back_btn = QPushButton()
        self.back_btn.setMinimumWidth(65)
        self.back_btn.clicked.connect(self.navigate_back)
        nav_layout.addWidget(self.back_btn)

        # Forward
        self.fwd_btn = QPushButton()
        self.fwd_btn.setMinimumWidth(65)
        self.fwd_btn.clicked.connect(self.navigate_forward)
        nav_layout.addWidget(self.fwd_btn)

        # Reload
        self.reload_btn = QPushButton()
        self.reload_btn.setMinimumWidth(75)
        self.reload_btn.clicked.connect(self.reload_page)
        nav_layout.addWidget(self.reload_btn)

        # Home
        self.home_btn = QPushButton()
        self.home_btn.setMinimumWidth(70)
        self.home_btn.clicked.connect(self.navigate_home)
        nav_layout.addWidget(self.home_btn)

        # Address Bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_address_url)
        nav_layout.addWidget(self.address_bar)

        # Zoom Out
        self.zoom_out_btn = QPushButton()
        self.zoom_out_btn.setMinimumWidth(60)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        nav_layout.addWidget(self.zoom_out_btn)

        # Zoom In
        self.zoom_in_btn = QPushButton()
        self.zoom_in_btn.setMinimumWidth(60)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        nav_layout.addWidget(self.zoom_in_btn)

        # Send to Downloader Button
        self.send_btn = QPushButton()
        self.send_btn.setProperty("class", "primary-btn")
        self.send_btn.setFixedHeight(34)
        self.send_btn.clicked.connect(self.on_send_to_downloader)
        nav_layout.addWidget(self.send_btn)

        layout.addWidget(nav_card, 0)

        # WebEngine View
        self.web_view = QWebEngineView()
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.web_view.urlChanged.connect(self.on_url_changed)
        self.web_view.titleChanged.connect(self.on_title_changed)

        layout.addWidget(self.web_view, 1)

        # Initial translate & load
        self.retranslate_ui()
        self.navigate_home()

    def retranslate_ui(self):
        lang = self.config.language
        self.back_btn.setText(tr("btn_back", lang))
        self.fwd_btn.setText(tr("btn_forward", lang))
        self.reload_btn.setText(tr("btn_reload", lang))
        self.home_btn.setText(tr("btn_home", lang))
        self.zoom_out_btn.setText(tr("btn_zoom_out", lang))
        self.zoom_in_btn.setText(tr("btn_zoom_in", lang))
        self.send_btn.setText(tr("btn_send_to_downloader", lang))
        self.address_bar.setPlaceholderText(tr("address_placeholder", lang))

    def zoom_in(self):
        self.web_view.setZoomFactor(min(self.web_view.zoomFactor() + 0.1, 3.0))

    def zoom_out(self):
        self.web_view.setZoomFactor(max(self.web_view.zoomFactor() - 0.1, 0.5))

    def navigate_home(self):
        url = self.config.website_url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.web_view.setUrl(QUrl(url))

    def load_address_url(self):
        url_text = self.address_bar.text().strip()
        if not url_text.startswith("http://") and not url_text.startswith("https://"):
            url_text = "https://" + url_text
        self.web_view.setUrl(QUrl(url_text))

    def navigate_back(self):
        self.web_view.back()

    def navigate_forward(self):
        self.web_view.forward()

    def reload_page(self):
        self.web_view.reload()

    def on_url_changed(self, qurl: QUrl):
        url_str = qurl.toString()
        self.address_bar.setText(url_str)
        self.back_btn.setEnabled(self.web_view.history().canGoBack())
        self.fwd_btn.setEnabled(self.web_view.history().canGoForward())

    def on_title_changed(self, title: str):
        pass

    def on_send_to_downloader(self):
        current_url = self.web_view.url().toString()
        if current_url:
            self.send_to_downloader.emit(current_url)
