import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLineEdit, QLabel, QHeaderView, QMessageBox, QFrame
)
from PySide6.QtCore import Signal, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from app.core.database import DatabaseManager
from app.core.i18n import tr

class HistoryTab(QWidget):
    """SQLite Download History Viewer Tab."""

    redownload_requested = Signal(dict)

    def __init__(self, db: DatabaseManager, config=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header & Search Bar Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        header_layout = QHBoxLayout(header_card)

        self.title_lbl = QLabel()
        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(260)
        self.search_input.textChanged.connect(self.load_history_data)
        header_layout.addWidget(self.search_input)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedWidth(34)
        refresh_btn.clicked.connect(self.load_history_data)
        header_layout.addWidget(refresh_btn)

        layout.addWidget(header_card)

        # History Tree Table Widget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(7)
        
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.tree.setAlternatingRowColors(True)
        layout.addWidget(self.tree)


        # Bottom Action Bar
        action_row = QHBoxLayout()

        self.open_folder_btn = QPushButton()
        self.open_folder_btn.clicked.connect(self.open_selected_folder)
        action_row.addWidget(self.open_folder_btn)

        self.redownload_btn = QPushButton()
        self.redownload_btn.setProperty("class", "primary-btn")
        self.redownload_btn.clicked.connect(self.on_redownload_clicked)
        action_row.addWidget(self.redownload_btn)

        action_row.addStretch()

        self.delete_btn = QPushButton()
        self.delete_btn.clicked.connect(self.delete_selected_record)
        action_row.addWidget(self.delete_btn)

        self.clear_all_btn = QPushButton()
        self.clear_all_btn.setProperty("class", "danger-btn")
        self.clear_all_btn.clicked.connect(self.clear_all_history)
        action_row.addWidget(self.clear_all_btn)

        layout.addLayout(action_row)

        self.retranslate_ui()
        self.load_history_data()

    def retranslate_ui(self):
        lang = self.config.language if self.config else "en"
        self.title_lbl.setText(f"<b>{tr('history_title', lang)}</b>")
        self.search_input.setPlaceholderText(tr("search_history_placeholder", lang))

        self.tree.setHeaderLabels([
            tr("col_id", lang),
            tr("col_title", lang),
            tr("col_episodes", lang),
            tr("col_quality", lang),
            tr("col_subtitles", lang),
            tr("col_status", lang),
            tr("col_datetime", lang),
        ])

        self.open_folder_btn.setText(tr("btn_open_folder", lang) + " 📁")
        self.redownload_btn.setText(tr("btn_redownload", lang))
        self.delete_btn.setText(tr("btn_delete_selected", lang))
        self.clear_all_btn.setText(tr("btn_clear_all", lang))

    def showEvent(self, event):
        super().showEvent(event)
        self.load_history_data()

    def load_history_data(self):
        query = self.search_input.text().strip()
        records = self.db.get_all_records(query)

        self.tree.clear()
        for r in records:
            title_display = r["title"]
            if len(title_display) > 50:
                title_display = title_display[:47] + "..."

            item = QTreeWidgetItem([
                str(r["id"]),
                title_display,
                r.get("episodes", "--"),
                r.get("quality", "--"),
                r.get("subtitle_lang", "--"),
                r.get("status", "--"),
                r.get("completed_at", "--"),
            ])
            item.setData(0, Qt.UserRole, r)
            self.tree.addTopLevelItem(item)

    def get_selected_record(self) -> dict:
        selected = self.tree.selectedItems()
        if selected:
            return selected[0].data(0, Qt.UserRole)
        return {}

    def open_selected_folder(self):
        rec = self.get_selected_record()
        if not rec:
            QMessageBox.warning(self, "No Selection", "Please select a history record first.")
            return

        folder_path = rec.get("output_dir", "")
        if folder_path and os.path.exists(folder_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        else:
            QMessageBox.warning(self, "Folder Not Found", f"Directory does not exist:\n{folder_path}")

    def on_redownload_clicked(self):
        rec = self.get_selected_record()
        if not rec:
            QMessageBox.warning(self, "No Selection", "Please select a history record to re-download.")
            return

        self.redownload_requested.emit(rec)

    def delete_selected_record(self):
        rec = self.get_selected_record()
        if not rec:
            QMessageBox.warning(self, "No Selection", "Please select a history record to delete.")
            return

        record_id = rec["id"]
        self.db.delete_record(record_id)
        self.load_history_data()

    def clear_all_history(self):
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to delete all download history records?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.db.clear_all_records()
            self.load_history_data()
