import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel,
    QPushButton, QCheckBox, QApplication, QFrame
)
from PySide6.QtGui import QFont, QTextCursor

class LogWidget(QWidget):
    """Activity Log Console Widget for displaying live application output."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Log Console Header
        header = QHBoxLayout()
        title_lbl = QLabel("<b>Activity Log Console</b>")
        header.addWidget(title_lbl)

        header.addStretch()

        self.auto_scroll_cb = QCheckBox("Auto-scroll")
        self.auto_scroll_cb.setChecked(True)
        header.addWidget(self.auto_scroll_cb)

        copy_btn = QPushButton("Copy")
        copy_btn.setFixedHeight(28)
        copy_btn.clicked.connect(self.copy_logs)
        header.addWidget(copy_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setFixedHeight(28)
        clear_btn.clicked.connect(self.clear_logs)
        header.addWidget(clear_btn)

        layout.addLayout(header)

        # Text Console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 9))
        self.console.setProperty("class", "console-edit")
        layout.addWidget(self.console)

    def log(self, level: str, message: str):
        """Append log line with level and timestamp."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        lvl_upper = level.upper()
        color = "#6366f1" # INFO Indigo
        if lvl_upper == "SUCCESS":
            color = "#10b981" # Green
        elif lvl_upper == "WARNING":
            color = "#d97706" # Amber
        elif lvl_upper == "ERROR":
            color = "#dc2626" # Red

        # Omit inline message color so message text inherits theme color dynamically!
        html_line = f'<span style="color:#64748b;">[{timestamp}]</span> ' \
                    f'<span style="color:{color}; font-weight:bold;">[{lvl_upper}]</span> ' \
                    f'<span>{message}</span><br/>'

        self.console.append(html_line)

        if self.auto_scroll_cb.isChecked():
            self.console.moveCursor(QTextCursor.End)

    def clear_logs(self):
        self.console.clear()

    def copy_logs(self):
        QApplication.clipboard().setText(self.console.toPlainText())
