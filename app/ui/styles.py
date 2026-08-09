FONT_STACK = "'Kantumruy Pro', 'Khmer OS Battambang', 'Khmer OS System', 'Hanuman', 'Segoe UI', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji', -apple-system, sans-serif"

DARK_THEME_QSS = f"""
/* Global Window & Typography */
QWidget {{
    background-color: #0f172a;
    color: #f8fafc;
    font-family: {FONT_STACK};
    font-size: 13px;
}}

/* Labels & Descriptions */
QLabel {{
    color: #f8fafc;
}}
QLabel.desc-text {{
    color: #94a3b8;
    font-size: 12px;
}}
QLabel.brand-title {{
    font-size: 19px;
    font-weight: bold;
    color: #818cf8;
}}
QLabel.brand-subtitle {{
    font-size: 11px;
    color: #94a3b8;
}}

/* Left Sidebar Panel */
QFrame.sidebar {{
    background-color: #0b0f19;
    border-right: 1px solid #1e293b;
    padding: 0px;
}}

QPushButton.nav-btn {{
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    margin-bottom: 4px;
}}
QPushButton.nav-btn:hover {{
    background-color: #1e293b;
    color: #f8fafc;
}}
QPushButton.nav-btn:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
    color: #ffffff;
    font-weight: bold;
}}

/* ScrollBars */
QScrollBar:vertical {{
    border: none;
    background: #1e293b;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #475569;
    min-height: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #64748b;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: #1e293b;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #475569;
    min-width: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #64748b;
}}

/* Card Containers */
QFrame.card {{
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
}}

QGroupBox {{
    font-weight: bold;
    border: 1px solid #334155;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #1e293b;
    color: #f8fafc;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    color: #818cf8;
}}

/* Input Fields */
QLineEdit, QComboBox, QSpinBox {{
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f8fafc;
    selection-background-color: #6366f1;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1.5px solid #818cf8;
}}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{
    border-color: #475569;
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: #1e293b;
    border: 1px solid #334155;
    selection-background-color: #4f46e5;
    color: #f8fafc;
}}

/* Checkboxes & Radio Buttons */
QCheckBox, QRadioButton {{
    spacing: 8px;
    color: #e2e8f0;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid #475569;
    background-color: #0f172a;
}}
QRadioButton::indicator {{
    border-radius: 9px;
}}
QCheckBox::indicator:checked {{
    background-color: #6366f1;
    border-color: #6366f1;
}}
QRadioButton::indicator:checked {{
    background-color: #6366f1;
    border-color: #818cf8;
}}

/* Buttons */
QPushButton {{
    background-color: #334155;
    color: #f8fafc;
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #475569;
}}
QPushButton:pressed {{
    background-color: #1e293b;
}}

QPushButton.primary-btn {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
    color: #ffffff;
}}
QPushButton.primary-btn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
}}
QPushButton.primary-btn:pressed {{
    background: #4338ca;
}}

QPushButton.secondary-btn {{
    background-color: #1e293b;
    border: 1px solid #6366f1;
    color: #818cf8;
}}
QPushButton.secondary-btn:hover {{
    background-color: #312e81;
    color: #ffffff;
}}

QPushButton.danger-btn {{
    background-color: #991b1b;
    color: #ffffff;
}}
QPushButton.danger-btn:hover {{
    background-color: #dc2626;
}}

/* Tables & Trees */
QTreeWidget {{
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    alternate-background-color: #0f172a;
}}
QHeaderView::section {{
    background-color: #0f172a;
    color: #818cf8;
    font-weight: bold;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #334155;
}}

/* Console Log TextEdit */
QTextEdit.console-edit {{
    background-color: #020617;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    height: 20px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #10b981);
    border-radius: 7px;
}}

/* Status Badge Card */
QLabel.badge-card {{
    background-color: #1e1b4b;
    color: #818cf8;
    font-weight: bold;
    padding: 8px 14px;
    border-radius: 10px;
    border: 1px solid #4338ca;
}}

/* Status Bar */
QStatusBar {{
    background-color: #0b0f19;
    color: #94a3b8;
    border-top: 1px solid #1e293b;
}}
"""

LIGHT_THEME_QSS = f"""
/* Global Window & Typography */
QWidget {{
    background-color: #f8fafc;
    color: #0f172a;
    font-family: {FONT_STACK};
    font-size: 13px;
}}

/* Labels & Descriptions */
QLabel {{
    color: #0f172a;
}}
QLabel.desc-text {{
    color: #475569;
    font-size: 12px;
}}
QLabel.brand-title {{
    font-size: 19px;
    font-weight: bold;
    color: #4338ca;
}}
QLabel.brand-subtitle {{
    font-size: 11px;
    color: #64748b;
}}

/* Left Sidebar Panel */
QFrame.sidebar {{
    background-color: #ffffff;
    border-right: 1.5px solid #cbd5e1;
    padding: 0px;
}}

QPushButton.nav-btn {{
    background-color: transparent;
    color: #334155;
    border: none;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
    margin-bottom: 4px;
}}
QPushButton.nav-btn:hover {{
    background-color: #e0e7ff;
    color: #1e1b4b;
}}
QPushButton.nav-btn:checked {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff;
    font-weight: bold;
}}

/* ScrollBars */
QScrollBar:vertical {{
    border: none;
    background: #f1f5f9;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #94a3b8;
    min-height: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #64748b;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: #f1f5f9;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #94a3b8;
    min-width: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #64748b;
}}

/* Card Containers */
QFrame.card {{
    background-color: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 16px;
}}

QGroupBox {{
    font-weight: bold;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #ffffff;
    color: #0f172a;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 6px;
    color: #3730a3;
    font-size: 14px;
}}

/* Input Fields */
QLineEdit, QComboBox, QSpinBox {{
    background-color: #ffffff;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0f172a;
    font-weight: 500;
    selection-background-color: #6366f1;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 2px solid #4f46e5;
}}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{
    border-color: #64748b;
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: #ffffff;
    border: 1.5px solid #cbd5e1;
    selection-background-color: #e0e7ff;
    color: #0f172a;
}}

/* Checkboxes & Radio Buttons */
QCheckBox, QRadioButton {{
    spacing: 8px;
    color: #0f172a;
    font-weight: 500;
}}
QCheckBox::indicator, QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1.5px solid #64748b;
    background-color: #ffffff;
}}
QRadioButton::indicator {{
    border-radius: 9px;
}}
QCheckBox::indicator:checked {{
    background-color: #4f46e5;
    border-color: #4f46e5;
}}
QRadioButton::indicator:checked {{
    background-color: #4f46e5;
    border-color: #3730a3;
}}

/* Buttons */
QPushButton {{
    background-color: #f1f5f9;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #e2e8f0;
}}
QPushButton:pressed {{
    background-color: #cbd5e1;
}}

QPushButton.primary-btn {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
}}
QPushButton.primary-btn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #6d28d9);
}}
QPushButton.primary-btn:pressed {{
    background: #3730a3;
}}

QPushButton.secondary-btn {{
    background-color: #eef2ff;
    border: 1.5px solid #6366f1;
    color: #3730a3;
}}
QPushButton.secondary-btn:hover {{
    background-color: #e0e7ff;
    color: #1e1b4b;
}}

QPushButton.danger-btn {{
    background-color: #dc2626;
    color: #ffffff;
    border: none;
}}
QPushButton.danger-btn:hover {{
    background-color: #b91c1c;
}}

/* Tables & Trees */
QTreeWidget {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    alternate-background-color: #f8fafc;
}}
QHeaderView::section {{
    background-color: #e0e7ff;
    color: #3730a3;
    font-weight: bold;
    font-size: 13px;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #c7d2fe;
}}

/* Console Log TextEdit */
QTextEdit.console-edit {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    text-align: center;
    color: #0f172a;
    font-weight: bold;
    height: 20px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #10b981);
    border-radius: 7px;
}}

/* Status Badge Card */
QLabel.badge-card {{
    background-color: #e0e7ff;
    color: #3730a3;
    font-weight: bold;
    padding: 8px 14px;
    border-radius: 10px;
    border: 1.5px solid #c7d2fe;
}}

/* Status Bar */
QStatusBar {{
    background-color: #ffffff;
    color: #334155;
    border-top: 1.5px solid #cbd5e1;
}}
"""

def get_theme_qss(theme_name: str) -> str:
    """Returns QSS string for target theme."""
    if theme_name.lower() == "light":
        return LIGHT_THEME_QSS
    return DARK_THEME_QSS
