import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from widgets.application import ApplicationWindow
from PySide6.QtGui import QIcon
from utils.dark_mode import is_dark_mode


if __name__ == "__main__":
    app = QApplication(sys.argv)


    is_dark_mode = is_dark_mode()
    icon_path = "assets/Logo_Dark.png" if is_dark_mode else "assets/Logo_Light.png"

    app.setStyle("font-family: 'Segoe UI';"
                 "font-size: 15pt;"
                 "text-align: left;")

    window = ApplicationWindow()
    window.setWindowIcon(QIcon(icon_path))


    # Mostrar en pantalla completa (modo ventana maximizada con barra y botones)
    window.showMaximized()

    # Permitir salir con tecla ESC
    window.keyPressEvent = lambda e: app.quit() if e.key() == Qt.Key_Escape else None

    sys.exit(app.exec())
