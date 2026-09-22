from typing import Dict, List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QProgressBar, QHeaderView, QMenu
)
from PySide6.QtCore import Signal, Qt
from app.core.i18n import tr

# Item data roles
ROLE_ID = Qt.UserRole          # group_id for movie rows, task_id for episode rows
ROLE_STATE = Qt.UserRole + 1   # episode state: queued|downloading|retrying|failed|completed
ROLE_INFO = Qt.UserRole + 2    # dict with error/attempt/progress text for re-rendering

MAX_AUTO_RETRIES = 2


class QueueTab(QWidget):
    """Download Queue Manager Tab. One parent row per movie, one child row per episode."""

    start_queue_requested = Signal()
    pause_queue_requested = Signal()
    cancel_task_requested = Signal(str)
    clear_completed_requested = Signal()
    retry_requested = Signal(list)          # task ids
    remove_group_requested = Signal(str)    # group id

    def __init__(self, config=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.group_items: Dict[str, QTreeWidgetItem] = {}
        self.task_items: Dict[str, QTreeWidgetItem] = {}
        self.init_ui()

    @property
    def lang(self) -> str:
        return self.config.language if self.config else "en"

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

        self.retry_failed_btn = QPushButton()
        self.retry_failed_btn.clicked.connect(lambda: self.retry_requested.emit(self.failed_task_ids()))
        toolbar.addWidget(self.retry_failed_btn)

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
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

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
        lang = self.lang
        self.title_lbl.setText(f"<b>{tr('queue_title', lang)}</b>")
        self.start_btn.setText(tr("btn_start_queue", lang))
        self.retry_failed_btn.setText(tr("btn_retry_failed", lang))
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
        for task_id in self.task_items:
            self._render_task(task_id)
        for group_id in self.group_items:
            self._refresh_group(group_id)

    # --- Building rows ---

    def _add_progress_bar(self, item: QTreeWidgetItem) -> QProgressBar:
        pb = QProgressBar()
        pb.setValue(0)
        pb.setFixedHeight(16)
        self.tree.setItemWidget(item, 4, pb)
        return pb

    def add_group(self, group_id: str, title: str, params: dict) -> QTreeWidgetItem:
        sub_text = "None"
        if params.get("enable_subtitles"):
            sub_text = f"{params.get('sub_lang', 'en').upper()}"
            if params.get("decrypt_subtitles"):
                sub_text += " (Decrypted)"

        item = QTreeWidgetItem([
            title,
            "",
            params.get("quality", "1080p"),
            sub_text,
            "",
            tr("status_resolving", self.lang),
        ])
        item.setData(0, ROLE_ID, group_id)
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
        self.tree.addTopLevelItem(item)
        self._add_progress_bar(item)
        item.setExpanded(True)
        self.group_items[group_id] = item
        return item

    def set_group_title(self, group_id: str, title: str):
        item = self.group_items.get(group_id)
        if item:
            item.setText(0, title)

    def set_group_error(self, group_id: str, message: str):
        item = self.group_items.get(group_id)
        if item:
            item.setText(5, message)

    def add_episode(self, group_id: str, task_id: str, episode: int,
                    state: str = "queued", error: str = "", attempt: int = 0) -> Optional[QTreeWidgetItem]:
        group = self.group_items.get(group_id)
        if group is None:
            return None
        item = QTreeWidgetItem([f"Episode {episode}", f"E{episode:02d}", "", "", "", ""])
        item.setData(0, ROLE_ID, task_id)
        item.setData(0, ROLE_STATE, state)
        item.setData(0, ROLE_INFO, {"error": error, "attempt": attempt, "text": ""})
        group.addChild(item)
        self._add_progress_bar(item)
        self.task_items[task_id] = item
        self._render_task(task_id)
        self._refresh_group(group_id)
        return item

    # --- Updating rows ---

    def set_task_state(self, task_id: str, state: str, error: str = "", attempt: int = 0):
        item = self.task_items.get(task_id)
        if not item:
            return
        item.setData(0, ROLE_STATE, state)
        item.setData(0, ROLE_INFO, {"error": error, "attempt": attempt, "text": ""})
        pb = self.tree.itemWidget(item, 4)
        if pb:
            if state == "completed":
                pb.setValue(100)
            elif state in ("queued", "retrying", "failed"):
                pb.setValue(0)
        self._render_task(task_id)
        self._refresh_group(item.parent().data(0, ROLE_ID))

    def update_task_progress(self, task_id: str, percent: int, speed: str, status: str):
        item = self.task_items.get(task_id)
        if not item:
            return
        pb = self.tree.itemWidget(item, 4)
        if pb:
            pb.setValue(percent)
        info = dict(item.data(0, ROLE_INFO) or {})
        info["text"] = f"{status} ({speed})" if speed else status
        item.setData(0, ROLE_INFO, info)
        self._render_task(task_id)
        self._refresh_group(item.parent().data(0, ROLE_ID))

    def _render_task(self, task_id: str):
        item = self.task_items[task_id]
        state = item.data(0, ROLE_STATE)
        info = item.data(0, ROLE_INFO) or {}
        lang = self.lang
        if state == "downloading":
            text = info.get("text") or tr("status_downloading", lang)
        elif state == "retrying":
            text = tr("status_retrying", lang, n=info.get("attempt", 1), max=MAX_AUTO_RETRIES)
        elif state == "failed":
            text = tr("status_failed", lang, error=info.get("error") or "?")
        elif state == "completed":
            text = tr("status_completed", lang)
        else:
            text = tr("status_queued", lang)
        item.setText(5, text)
        item.setToolTip(5, text)

    def _refresh_group(self, group_id: str):
        group = self.group_items.get(group_id)
        if not group or group.childCount() == 0:
            return
        states = []
        total_progress = 0
        downloading_ep = ""
        for i in range(group.childCount()):
            child = group.child(i)
            state = child.data(0, ROLE_STATE)
            states.append(state)
            pb = self.tree.itemWidget(child, 4)
            total_progress += 100 if state == "completed" else (pb.value() if pb else 0)
            if state == "downloading":
                downloading_ep = child.text(1)

        total = len(states)
        done = states.count("completed")
        failed = states.count("failed")
        lang = self.lang
        group.setText(1, tr("status_eps_done", lang, done=done, total=total))
        pb = self.tree.itemWidget(group, 4)
        if pb:
            pb.setValue(int(total_progress / total))

        parts = []
        if downloading_ep:
            parts.append(f"{tr('status_downloading', lang)} {downloading_ep}")
        if failed:
            parts.append(tr("status_group_failed", lang, count=failed))
        if done == total:
            parts.append(tr("status_completed", lang))
        elif not parts:
            parts.append(tr("status_queued", lang))
        group.setText(5, " · ".join(parts))

    # --- Queries / removal ---

    def failed_task_ids(self, group_id: Optional[str] = None) -> List[str]:
        return [
            task_id for task_id, item in self.task_items.items()
            if item.data(0, ROLE_STATE) == "failed"
            and (group_id is None or item.parent().data(0, ROLE_ID) == group_id)
        ]

    def group_task_ids(self, group_id: str) -> List[str]:
        group = self.group_items.get(group_id)
        if not group:
            return []
        return [group.child(i).data(0, ROLE_ID) for i in range(group.childCount())]

    def remove_group(self, group_id: str):
        for task_id in self.group_task_ids(group_id):
            self.task_items.pop(task_id, None)
        group = self.group_items.pop(group_id, None)
        if group:
            self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(group))

    def remove_completed_items(self) -> List[str]:
        """Removes completed episodes (and groups left empty). Returns removed task ids."""
        removed = []
        for group_id, group in list(self.group_items.items()):
            for i in reversed(range(group.childCount())):
                child = group.child(i)
                if child.data(0, ROLE_STATE) == "completed":
                    task_id = child.data(0, ROLE_ID)
                    self.task_items.pop(task_id, None)
                    group.takeChild(i)
                    removed.append(task_id)
            if group.childCount() == 0 and group.text(5) != tr("status_resolving", self.lang):
                self.remove_group(group_id)
            else:
                self._refresh_group(group_id)
        return removed

    # --- Context menu ---

    def show_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if not item:
            return
        lang = self.lang
        menu = QMenu(self)
        item_id = item.data(0, ROLE_ID)

        if item.parent() is None:  # movie row
            failed = self.failed_task_ids(item_id)
            retry_action = menu.addAction(tr("menu_retry_group", lang))
            retry_action.setEnabled(bool(failed))
            retry_action.triggered.connect(lambda: self.retry_requested.emit(failed))
            remove_action = menu.addAction(tr("menu_remove_group", lang))
            remove_action.triggered.connect(lambda: self.remove_group_requested.emit(item_id))
        else:  # episode row
            state = item.data(0, ROLE_STATE)
            retry_action = menu.addAction(tr("menu_retry", lang))
            retry_action.setEnabled(state == "failed")
            retry_action.triggered.connect(lambda: self.retry_requested.emit([item_id]))
            cancel_action = menu.addAction(tr("menu_cancel", lang))
            cancel_action.setEnabled(state in ("downloading", "queued", "retrying"))
            cancel_action.triggered.connect(lambda: self.cancel_task_requested.emit(item_id))

        menu.exec(self.tree.viewport().mapToGlobal(pos))
