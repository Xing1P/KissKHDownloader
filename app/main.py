import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import Qt

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ui.main_window import MainWindow

def load_custom_fonts():
    """Loads bundled custom TTF fonts into Qt QFontDatabase."""
    fonts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "fonts"))
    if os.path.exists(fonts_dir):
        for font_file in os.listdir(fonts_dir):
            if font_file.lower().endswith((".ttf", ".otf")):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"Registered font: {families}")

def main():
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("KissKH Downloader Qt")
    app.setOrganizationName("KissKH")

    # Load App Icon
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "icon.png"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Load Kantumruy Pro font
    load_custom_fonts()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
