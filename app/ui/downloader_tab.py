import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QCheckBox, QRadioButton,
    QButtonGroup, QSpinBox, QGroupBox, QFileDialog, QApplication, QFrame
)
from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QDesktopServices
from app.core.config import AppConfig
from app.core.i18n import tr

class DownloaderTab(QWidget):
    """Main Form tab for configuring and launching KissKH downloads."""

    download_requested = Signal(dict)
    add_queue_requested = Signal(dict)

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Section 1: URL / Search Input Card ---
        url_card = QFrame()
        url_card.setProperty("class", "card")
        url_layout = QVBoxLayout(url_card)

        self.url_label = QLabel()
        url_layout.addWidget(self.url_label)

        input_row = QHBoxLayout()
        self.url_input = QLineEdit()
        input_row.addWidget(self.url_input)

        self.paste_btn = QPushButton()
        self.paste_btn.clicked.connect(self.paste_from_clipboard)
        input_row.addWidget(self.paste_btn)

        url_layout.addLayout(input_row)
        main_layout.addWidget(url_card)

        # --- Section 2: Download Options Grid ---
        options_grid = QGridLayout()

        # Group 1: Episodes Selection
        self.ep_group = QGroupBox()
        ep_layout = QVBoxLayout(self.ep_group)

        self.ep_bg = QButtonGroup(self)
        self.rb_all_ep = QRadioButton()
        self.rb_all_ep.setChecked(True)
        self.ep_bg.addButton(self.rb_all_ep, 1)
        ep_layout.addWidget(self.rb_all_ep)

        # Single episode row
        single_row = QHBoxLayout()
        self.rb_single_ep = QRadioButton()
        self.ep_bg.addButton(self.rb_single_ep, 2)
        single_row.addWidget(self.rb_single_ep)

        self.single_ep_spin = QSpinBox()
        self.single_ep_spin.setRange(1, 9999)
        self.single_ep_spin.setValue(1)
        self.single_ep_spin.setEnabled(False)
        single_row.addWidget(self.single_ep_spin)
        single_row.addStretch()
        ep_layout.addLayout(single_row)

        # Range row
        range_row = QHBoxLayout()
        self.rb_range_ep = QRadioButton()
        self.ep_bg.addButton(self.rb_range_ep, 3)
        range_row.addWidget(self.rb_range_ep)

        self.lbl_from = QLabel()
        range_row.addWidget(self.lbl_from)
        self.from_ep_spin = QSpinBox()
        self.from_ep_spin.setRange(1, 9999)
        self.from_ep_spin.setValue(1)
        self.from_ep_spin.setEnabled(False)
        range_row.addWidget(self.from_ep_spin)

        self.lbl_to = QLabel()
        range_row.addWidget(self.lbl_to)
        self.to_ep_spin = QSpinBox()
        self.to_ep_spin.setRange(1, 9999)
        self.to_ep_spin.setValue(10)
        self.to_ep_spin.setEnabled(False)
        range_row.addWidget(self.to_ep_spin)
        range_row.addStretch()
        ep_layout.addLayout(range_row)

        self.ep_bg.idToggled.connect(self.on_episode_mode_changed)
        options_grid.addWidget(self.ep_group, 0, 0)

        # Group 2: Quality & Subtitles
        self.settings_group = QGroupBox()
        settings_layout = QGridLayout(self.settings_group)

        self.lbl_quality = QLabel()
        settings_layout.addWidget(self.lbl_quality, 0, 0)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["1080p", "720p", "480p", "360p", "Best Available"])
        idx = self.quality_combo.findText(self.config.default_quality)
        if idx >= 0:
            self.quality_combo.setCurrentIndex(idx)
        settings_layout.addWidget(self.quality_combo, 0, 1)

        self.sub_enable_cb = QCheckBox()
        self.sub_enable_cb.setChecked(self.config.enable_subtitles)
        settings_layout.addWidget(self.sub_enable_cb, 1, 0)

        self.sub_lang_combo = QComboBox()
        self.sub_lang_combo.addItem("English (en)", "en")
        self.sub_lang_combo.addItem("Indonesian (id)", "id")
        self.sub_lang_combo.addItem("Spanish (es)", "es")
        self.sub_lang_combo.addItem("Vietnamese (vi)", "vi")
        self.sub_lang_combo.addItem("Thai (th)", "th")
        self.sub_lang_combo.addItem("Portuguese (pt)", "pt")
        self.sub_lang_combo.addItem("Arabic (ar)", "ar")
        self.sub_lang_combo.addItem("All Languages (all)", "all")
        lang_idx = self.sub_lang_combo.findData(self.config.subtitle_language)
        if lang_idx >= 0:
            self.sub_lang_combo.setCurrentIndex(lang_idx)
        settings_layout.addWidget(self.sub_lang_combo, 1, 1)

        self.sub_decrypt_cb = QCheckBox()
        self.sub_decrypt_cb.setChecked(self.config.decrypt_subtitles)
        settings_layout.addWidget(self.sub_decrypt_cb, 2, 0, 1, 2)

        self.sub_enable_cb.toggled.connect(self.sub_lang_combo.setEnabled)
        self.sub_enable_cb.toggled.connect(self.sub_decrypt_cb.setEnabled)

        options_grid.addWidget(self.settings_group, 0, 1)
        main_layout.addLayout(options_grid)

        # --- Section 3: Output Folder Card ---
        folder_card = QFrame()
        folder_card.setProperty("class", "card")
        folder_layout = QVBoxLayout(folder_card)

        self.folder_title_lbl = QLabel()
        folder_layout.addWidget(self.folder_title_lbl)
        folder_row = QHBoxLayout()

        self.folder_input = QLineEdit()
        self.folder_input.setText(self.config.default_output_dir)
        folder_row.addWidget(self.folder_input)

        self.browse_btn = QPushButton()
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_row.addWidget(self.browse_btn)

        self.open_folder_btn = QPushButton()
        self.open_folder_btn.clicked.connect(self.open_destination_folder)
        folder_row.addWidget(self.open_folder_btn)

        folder_layout.addLayout(folder_row)
        main_layout.addWidget(folder_card)

        # --- Section 4: Action Buttons ---
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.add_queue_btn = QPushButton()
        self.add_queue_btn.setProperty("class", "secondary-btn")
        self.add_queue_btn.setFixedHeight(40)
        self.add_queue_btn.clicked.connect(self.on_add_to_queue)
        action_layout.addWidget(self.add_queue_btn)

        self.download_now_btn = QPushButton()
        self.download_now_btn.setProperty("class", "primary-btn")
        self.download_now_btn.setFixedHeight(40)
        self.download_now_btn.setMinimumWidth(180)
        self.download_now_btn.clicked.connect(self.on_download_now)
        action_layout.addWidget(self.download_now_btn)

        main_layout.addLayout(action_layout)
        main_layout.addStretch()

        # Translate
        self.retranslate_ui()

    def retranslate_ui(self):
        lang = self.config.language
        self.url_label.setText(f"<b>{tr('url_card_title', lang)}</b>")
        self.url_input.setPlaceholderText(tr("url_placeholder", lang))
        self.paste_btn.setText(tr("btn_paste", lang))

        self.ep_group.setTitle(tr("group_episodes", lang))
        self.rb_all_ep.setText(tr("rb_all_episodes", lang))
        self.rb_single_ep.setText(tr("rb_single_episode", lang))
        self.rb_range_ep.setText(tr("rb_range_episodes", lang))
        self.lbl_from.setText(tr("lbl_from", lang))
        self.lbl_to.setText(tr("lbl_to", lang))

        self.settings_group.setTitle(tr("group_quality_sub", lang))
        self.lbl_quality.setText(tr("lbl_quality", lang))
        self.sub_enable_cb.setText(tr("chk_subtitles", lang))
        self.sub_decrypt_cb.setText(tr("chk_decrypt_sub", lang))

        self.folder_title_lbl.setText(f"<b>{tr('card_folder_title', lang)}</b>")
        self.browse_btn.setText(tr("btn_browse", lang))
        self.open_folder_btn.setText(tr("btn_open_folder", lang))

        self.add_queue_btn.setText(tr("btn_add_queue", lang))
        self.download_now_btn.setText(tr("btn_download_now", lang))

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.url_input.setText(text)

    def on_episode_mode_changed(self, button_id: int, checked: bool):
        if not checked:
            return
        self.single_ep_spin.setEnabled(button_id == 2)
        self.from_ep_spin.setEnabled(button_id == 3)
        self.to_ep_spin.setEnabled(button_id == 3)

    def browse_folder(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Save Folder", self.folder_input.text()
        )
        if dir_path:
            self.folder_input.setText(dir_path)
            self.config.default_output_dir = dir_path

    def open_destination_folder(self):
        folder_path = self.folder_input.text()
        if os.path.exists(folder_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    def get_form_data(self) -> dict:
        url_or_name = self.url_input.text().strip()
        output_dir = self.folder_input.text().strip()
        quality = self.quality_combo.currentText().replace(" Available", "")
        
        mode = self.ep_bg.checkedId()
        all_episodes = (mode == 1)
        first_ep = None
        last_ep = None

        if mode == 2:
            first_ep = self.single_ep_spin.value()
            last_ep = self.single_ep_spin.value()
        elif mode == 3:
            first_ep = self.from_ep_spin.value()
            last_ep = self.to_ep_spin.value()

        enable_subtitles = self.sub_enable_cb.isChecked()
        sub_lang = self.sub_lang_combo.currentData()
        decrypt_subtitles = self.sub_decrypt_cb.isChecked()

        return {
            "url_or_name": url_or_name,
            "output_dir": output_dir,
            "quality": quality,
            "all_episodes": all_episodes,
            "first_ep": first_ep,
            "last_ep": last_ep,
            "enable_subtitles": enable_subtitles,
            "sub_lang": sub_lang,
            "decrypt_subtitles": decrypt_subtitles,
        }

    def on_download_now(self):
        data = self.get_form_data()
        self.download_requested.emit(data)

    def on_add_to_queue(self):
        data = self.get_form_data()
        self.add_queue_requested.emit(data)
