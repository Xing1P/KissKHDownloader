from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QComboBox, QCheckBox,
    QMessageBox, QFrame
)
from PySide6.QtCore import Signal
from app.__version__ import __version__, __app_name__
from app.core.config import AppConfig
from app.core.worker import PlaywrightInstallWorker, GetKeyWorker
from app.core.i18n import tr



class SettingsTab(QWidget):
    """Application Settings, Theme, Language, and Authentication Key Configuration Tab."""

    settings_saved = Signal()
    log_signal = Signal(str, str) # level, msg

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.pw_worker = None
        self.get_key_worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # --- Section 1: Theme & Language ---
        self.theme_lang_group = QGroupBox()
        tl_layout = QGridLayout(self.theme_lang_group)

        self.lbl_theme = QLabel()
        tl_layout.addWidget(self.lbl_theme, 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Dark Mode (ងងឹត)", "dark")
        self.theme_combo.addItem("Light Mode (ភ្លឺ)", "light")
        t_idx = self.theme_combo.findData(self.config.theme)
        if t_idx >= 0:
            self.theme_combo.setCurrentIndex(t_idx)
        tl_layout.addWidget(self.theme_combo, 0, 1)

        self.lbl_language = QLabel()
        tl_layout.addWidget(self.lbl_language, 1, 0)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("ភាសាខ្មែរ (Khmer)", "km")
        l_idx = self.lang_combo.findData(self.config.language)
        if l_idx >= 0:
            self.lang_combo.setCurrentIndex(l_idx)
        tl_layout.addWidget(self.lang_combo, 1, 1)

        layout.addWidget(self.theme_lang_group)

        # --- Section 2: Authentication Keys ---
        self.key_group = QGroupBox()
        key_layout = QGridLayout(self.key_group)

        self.lbl_stream_key = QLabel()
        key_layout.addWidget(self.lbl_stream_key, 0, 0)
        self.stream_key_input = QLineEdit()
        self.stream_key_input.setEchoMode(QLineEdit.Password)
        self.stream_key_input.setText(self.config.stream_key)
        key_layout.addWidget(self.stream_key_input, 0, 1)

        self.lbl_sub_key = QLabel()
        key_layout.addWidget(self.lbl_sub_key, 1, 0)
        self.sub_key_input = QLineEdit()
        self.sub_key_input.setEchoMode(QLineEdit.Password)
        self.sub_key_input.setText(self.config.sub_key)
        key_layout.addWidget(self.sub_key_input, 1, 1)

        self.lbl_decrypt_key = QLabel()
        key_layout.addWidget(self.lbl_decrypt_key, 2, 0)
        self.decrypt_key_input = QLineEdit()
        self.decrypt_key_input.setEchoMode(QLineEdit.Password)
        self.decrypt_key_input.setText(self.config.decrypt_key)
        key_layout.addWidget(self.decrypt_key_input, 2, 1)

        self.lbl_decrypt_iv = QLabel()
        key_layout.addWidget(self.lbl_decrypt_iv, 3, 0)
        self.decrypt_iv_input = QLineEdit()
        self.decrypt_iv_input.setEchoMode(QLineEdit.Password)
        self.decrypt_iv_input.setText(self.config.decrypt_iv)
        key_layout.addWidget(self.decrypt_iv_input, 3, 1)

        self.show_keys_cb = QCheckBox()
        self.show_keys_cb.toggled.connect(self.toggle_keys_visibility)
        key_layout.addWidget(self.show_keys_cb, 4, 0, 1, 2)

        layout.addWidget(self.key_group)

        # --- Section 3: Playwright Auto-Key Generation ---
        pw_card = QFrame()
        pw_card.setProperty("class", "card")
        pw_layout = QVBoxLayout(pw_card)

        self.pw_title_lbl = QLabel()
        pw_layout.addWidget(self.pw_title_lbl)
        self.pw_desc_lbl = QLabel()
        self.pw_desc_lbl.setWordWrap(True)
        self.pw_desc_lbl.setProperty("class", "desc-text")
        pw_layout.addWidget(self.pw_desc_lbl)


        pw_row = QHBoxLayout()
        self.pw_status_label = QLabel("Status: Ready")
        pw_row.addWidget(self.pw_status_label)
        pw_row.addStretch()

        self.install_pw_btn = QPushButton()
        self.install_pw_btn.setProperty("class", "secondary-btn")
        self.install_pw_btn.clicked.connect(self.install_playwright)
        pw_row.addWidget(self.install_pw_btn)

        pw_layout.addLayout(pw_row)
        layout.addWidget(pw_card)

        # --- Section 4: One-Click Fetch Keys from Episode URL ---
        fetch_card = QFrame()
        fetch_card.setProperty("class", "card")
        fetch_layout = QVBoxLayout(fetch_card)

        self.fetch_title_lbl = QLabel()
        fetch_layout.addWidget(self.fetch_title_lbl)
        self.fetch_desc_lbl = QLabel()
        self.fetch_desc_lbl.setWordWrap(True)
        self.fetch_desc_lbl.setProperty("class", "desc-text")
        fetch_layout.addWidget(self.fetch_desc_lbl)


        fetch_row = QHBoxLayout()
        self.get_key_url_input = QLineEdit()
        fetch_row.addWidget(self.get_key_url_input)

        self.fetch_keys_btn = QPushButton()
        self.fetch_keys_btn.setProperty("class", "primary-btn")
        self.fetch_keys_btn.clicked.connect(self.on_fetch_keys_clicked)
        fetch_row.addWidget(self.fetch_keys_btn)

        fetch_layout.addLayout(fetch_row)
        layout.addWidget(fetch_card)

        # --- Section 5: Default Download Preferences ---
        self.pref_group = QGroupBox()
        pref_layout = QGridLayout(self.pref_group)

        self.lbl_def_quality = QLabel()
        pref_layout.addWidget(self.lbl_def_quality, 0, 0)
        self.def_quality_combo = QComboBox()
        self.def_quality_combo.addItems(["1080p", "720p", "480p", "360p", "Best Available"])
        idx = self.def_quality_combo.findText(self.config.default_quality)
        if idx >= 0:
            self.def_quality_combo.setCurrentIndex(idx)
        pref_layout.addWidget(self.def_quality_combo, 0, 1)

        self.lbl_def_sub_lang = QLabel()
        pref_layout.addWidget(self.lbl_def_sub_lang, 1, 0)
        self.def_sub_combo = QComboBox()
        self.def_sub_combo.addItem("English (en)", "en")
        self.def_sub_combo.addItem("Indonesian (id)", "id")
        self.def_sub_combo.addItem("Spanish (es)", "es")
        self.def_sub_combo.addItem("Vietnamese (vi)", "vi")
        self.def_sub_combo.addItem("Thai (th)", "th")
        self.def_sub_combo.addItem("Portuguese (pt)", "pt")
        self.def_sub_combo.addItem("Arabic (ar)", "ar")
        self.def_sub_combo.addItem("All Languages (all)", "all")
        s_idx = self.def_sub_combo.findData(self.config.subtitle_language)
        if s_idx >= 0:
            self.def_sub_combo.setCurrentIndex(s_idx)
        pref_layout.addWidget(self.def_sub_combo, 1, 1)

        self.lbl_website_url = QLabel()
        pref_layout.addWidget(self.lbl_website_url, 2, 0)
        self.website_url_input = QLineEdit()
        self.website_url_input.setText(self.config.website_url)
        self.website_url_input.setPlaceholderText("e.g., https://kisskh.is/")
        pref_layout.addWidget(self.website_url_input, 2, 1)

        layout.addWidget(self.pref_group)

        # --- Section 6: About & Application Version ---
        about_card = QFrame()
        about_card.setProperty("class", "card")
        about_layout = QHBoxLayout(about_card)

        self.about_lbl = QLabel(f"<b>{__app_name__}</b> — Version <b>v{__version__}</b>")
        about_layout.addWidget(self.about_lbl)
        about_layout.addStretch()

        layout.addWidget(about_card)


        # Save Button
        save_row = QHBoxLayout()
        save_row.addStretch()

        self.save_btn = QPushButton()
        self.save_btn.setProperty("class", "primary-btn")
        self.save_btn.setFixedHeight(40)
        self.save_btn.setMinimumWidth(150)
        self.save_btn.clicked.connect(self.save_settings)
        save_row.addWidget(self.save_btn)

        layout.addLayout(save_row)
        layout.addStretch()

        self.retranslate_ui()

    def retranslate_ui(self):
        lang = self.config.language
        self.theme_lang_group.setTitle(tr("group_theme_lang", lang))
        self.lbl_theme.setText(tr("lbl_theme", lang))
        self.lbl_language.setText(tr("lbl_language", lang))

        self.key_group.setTitle(tr("group_keys", lang))
        self.lbl_stream_key.setText(tr("lbl_stream_key", lang))
        self.lbl_sub_key.setText(tr("lbl_sub_key", lang))
        self.lbl_decrypt_key.setText(tr("lbl_decrypt_key", lang))
        self.lbl_decrypt_iv.setText(tr("lbl_decrypt_iv", lang))
        self.show_keys_cb.setText(tr("chk_show_keys", lang))

        self.pw_title_lbl.setText(f"<b>{tr('card_playwright_title', lang)}</b>")
        self.pw_desc_lbl.setText(tr("playwright_desc", lang))
        self.install_pw_btn.setText(tr("btn_install_playwright", lang))

        self.fetch_title_lbl.setText(f"<b>{tr('card_get_key_title', lang)}</b>")
        self.fetch_desc_lbl.setText(tr("get_key_desc", lang))
        self.fetch_keys_btn.setText(tr("btn_fetch_keys", lang))

        self.pref_group.setTitle(tr("group_pref", lang))
        self.lbl_def_quality.setText(tr("lbl_def_quality", lang))
        self.lbl_def_sub_lang.setText(tr("lbl_def_sub_lang", lang))
        self.lbl_website_url.setText(tr("lbl_website_url", lang))
        self.save_btn.setText(tr("btn_save_settings", lang))

    def toggle_keys_visibility(self, checked: bool):
        mode = QLineEdit.Normal if checked else QLineEdit.Password
        self.stream_key_input.setEchoMode(mode)
        self.sub_key_input.setEchoMode(mode)
        self.decrypt_key_input.setEchoMode(mode)
        self.decrypt_iv_input.setEchoMode(mode)

    def install_playwright(self):
        self.install_pw_btn.setEnabled(False)
        self.pw_status_label.setText("Installing Playwright Chromium...")
        self.pw_worker = PlaywrightInstallWorker()
        self.pw_worker.log_signal.connect(self.log_signal.emit)
        self.pw_worker.finished_signal.connect(self.on_pw_install_finished)
        self.pw_worker.start()

    def on_pw_install_finished(self, success: bool, message: str):
        self.install_pw_btn.setEnabled(True)
        if success:
            self.pw_status_label.setText("Status: Chromium Installed Successfully ✓")
            QMessageBox.information(self, "Playwright Installed", message)
        else:
            self.pw_status_label.setText("Status: Installation Failed")
            QMessageBox.critical(self, "Installation Error", message)

    def on_fetch_keys_clicked(self):
        url = self.get_key_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a valid KissKH Episode URL to fetch keys.")
            return

        self.fetch_keys_btn.setEnabled(False)
        self.fetch_keys_btn.setText("Extracting Keys...")
        self.get_key_worker = GetKeyWorker(url)
        self.get_key_worker.log_signal.connect(self.log_signal.emit)
        self.get_key_worker.finished_signal.connect(self.on_get_key_finished)
        self.get_key_worker.start()

    def on_get_key_finished(self, success: bool, stream_key: str, sub_key: str, message: str):
        self.fetch_keys_btn.setEnabled(True)
        self.fetch_keys_btn.setText(tr("btn_fetch_keys", self.config.language))
        if success:
            if stream_key:
                self.stream_key_input.setText(stream_key)
                self.config.stream_key = stream_key
            if sub_key:
                self.sub_key_input.setText(sub_key)
                self.config.sub_key = sub_key

            QMessageBox.information(self, "Keys Extracted", f"Keys fetched successfully!\n\nStream Key: {stream_key[:20]}...\nSub Key: {sub_key[:20]}...")
        else:
            QMessageBox.critical(self, "Key Extraction Failed", message)

    def save_settings(self):
        self.config.theme = self.theme_combo.currentData()
        self.config.language = self.lang_combo.currentData()
        self.config.stream_key = self.stream_key_input.text().strip()
        self.config.sub_key = self.sub_key_input.text().strip()
        self.config.decrypt_key = self.decrypt_key_input.text().strip()
        self.config.decrypt_iv = self.decrypt_iv_input.text().strip()
        self.config.default_quality = self.def_quality_combo.currentText()
        self.config.subtitle_language = self.def_sub_combo.currentData()
        
        web_url = self.website_url_input.text().strip()
        if web_url:
            self.config.website_url = web_url

        QMessageBox.information(self, "Settings Saved", "Application settings have been updated.")
        self.settings_saved.emit()
