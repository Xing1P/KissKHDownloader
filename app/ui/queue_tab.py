from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QProgressBar, QHeaderView
)
from PySide6.QtCore import Signal, Qt
from app.core.i18n import tr

class QueueTab(QWidget):
    """Download Queue Manager Tab."""

    start_queue_requested = Signal()
    pause_queue_requested = Signal()
    cancel_task_requested = Signal(str)
    clear_completed_requested = Signal()

    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Top Control Toolbar
        toolbar = QHBoxLayout()
        self.title_lbl = QLabel()
        toolbar.addWidget(self.title_lbl)
        toolbar.addStretch()

        self.start_btn = QPushButton()
        self.start_btn.setProperty("class", "primary-btn")
        self.start_btn.clicked.connect(self.start_queue_requested.emit)
        toolbar.addWidget(self.start_btn)

        self.pause_btn = QPushButton()
        self.pause_btn.clicked.connect(self.pause_queue_requested.emit)
        toolbar.addWidget(self.pause_btn)

        self.clear_btn = QPushButton()
        self.clear_btn.clicked.connect(self.clear_completed_requested.emit)
        toolbar.addWidget(self.clear_btn)

        layout.addLayout(toolbar)

        # Queue Tree Widget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(6)
        
        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.resizeSection(4, 180)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.tree.setAlternatingRowColors(True)
        layout.addWidget(self.tree)


        self.retranslate_ui()

    def retranslate_ui(self):
        lang = self.config.language if self.config else "en"
        self.title_lbl.setText(f"<b>{tr('queue_title', lang)}</b>")
        self.start_btn.setText(tr("btn_start_queue", lang))
        self.pause_btn.setText(tr("btn_pause_queue", lang))
        self.clear_btn.setText(tr("btn_clear_completed", lang))

        self.tree.setHeaderLabels([
            tr("col_title", lang),
            tr("col_episodes", lang),
            tr("col_quality", lang),
            tr("col_subtitles", lang),
            tr("col_progress", lang),
            tr("col_status", lang),
        ])

    def add_queue_item(self, task_id: str, data: dict) -> QTreeWidgetItem:
        url_text = data.get("url_or_name", "")
        if len(url_text) > 40:
            url_text = url_text[:37] + "..."

        ep_text = "All"
        if not data.get("all_episodes"):
            ep_text = f"{data.get('first_ep')} - {data.get('last_ep')}"

        sub_text = "None"
        if data.get("enable_subtitles"):
            sub_text = f"{data.get('sub_lang', 'en').upper()}"
            if data.get("decrypt_subtitles"):
                sub_text += " (Decrypted)"

        item = QTreeWidgetItem([
            url_text,
            ep_text,
            data.get("quality", "1080p"),
            sub_text,
            "",
            "Queued"
        ])
        item.setData(0, Qt.UserRole, task_id)
        self.tree.addTopLevelItem(item)

        pb = QProgressBar()
        pb.setValue(0)
        pb.setFixedHeight(16)
        self.tree.setItemWidget(item, 4, pb)

        return item

    def find_item_by_task_id(self, task_id: str) -> QTreeWidgetItem:
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.data(0, Qt.UserRole) == task_id:
                return item
        return None

    def update_task_progress(self, task_id: str, percent: int, speed: str, status: str):
        item = self.find_item_by_task_id(task_id)
        if item:
            pb = self.tree.itemWidget(item, 4)
            if pb:
                pb.setValue(percent)
            item.setText(5, f"{status} ({speed})" if speed else status)

    def update_task_status(self, task_id: str, status_text: str):
        item = self.find_item_by_task_id(task_id)
        if item:
            item.setText(5, status_text)

    def remove_completed_items(self):
        items_to_remove = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            status = item.text(5)
            if "Completed" in status or "Done" in status:
                items_to_remove.append(item)
        
        for item in items_to_remove:
            index = self.tree.indexOfTopLevelItem(item)
            self.tree.takeTopLevelItem(index)
