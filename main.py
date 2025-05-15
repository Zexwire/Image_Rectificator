import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from widgets.application import ApplicationWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("font-family: 'Segoe UI';"
                 "font-size: 15pt;"
                 "text-align: left;"
                 )

    window = ApplicationWindow()
    window.setMinimumSize(1100, 700)
    window.showFullScreen()
    # Add escape key to close application
    window.setWindowFlags(window.windowFlags() | Qt.WindowCloseButtonHint)
    window.keyPressEvent = lambda e: app.quit() if e.key() == Qt.Key_Escape else None
    window.show()

    sys.exit(app.exec())