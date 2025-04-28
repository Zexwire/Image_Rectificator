from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QFrame, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QPainter, QPen, QMouseEvent, QPixmap, QFont, QPalette, QIcon
from PySide6.QtCore import Qt, Signal, QLineF
import sys

from infinity_line import calculate_infinity_line
from classes import *

class ClickArea(QFrame):
    points_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.coordenadas = Coordenadas()
        self.image = None
        self.setStyleSheet("background-color: #808080;")
        self.setMinimumSize(800, 800)
        self.point_radius = 10  # Radio para detectar clics en puntos existentes
        self.infinity_line = None  # DEBUG:  borrar después

    def load_image(self, image_path):
        original_image = QPixmap(image_path)
        available_width = self.parent().width() - 40
        available_height = self.parent().height() - 40

        scaled_image = original_image.scaled(
            available_width, available_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.image = scaled_image
        self.setFixedSize(scaled_image.size())
        self.coordenadas.clear()
        self.points_changed.emit()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.image:
            x = event.position().x()
            y = event.position().y()

            # Primero verificar si se hizo clic en un punto existente
            if self.coordenadas.remove_point_near(x, y, self.point_radius):
                self.points_changed.emit()
                self.update()
            elif not self.coordenadas.is_complete():
                self.coordenadas.add_point(x, y)
                self.points_changed.emit()
                self.update()

    # DEBUG: Borrar después
    def set_infinity_line(self, infinity_line):
        self.infinity_line = infinity_line
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        if self.image:
            painter.drawPixmap(0, 0, self.image)

        if self.coordenadas.points:

            # El cambio de color está para debuggear el orden de los puntos. Se puede cambiar de vuelta a siempre rojo una vez sepamos que va bien
            # COLORS
            colors = [Qt.GlobalColor.red, Qt.GlobalColor.green, Qt.GlobalColor.blue, Qt.GlobalColor.yellow]
            # Dibujar puntos
            for i, point in enumerate(self.coordenadas.points):
                pen = QPen(colors[i])
                pen.setWidth(8)
                painter.setPen(pen)
                painter.drawPoint(int(point.x), int(point.y))

        # DEBUG: Para ver si se están calculando bien los puntos intersección. Cuando terminemos con el primer sprint lo borramos
        if self.infinity_line and len(self.coordenadas.points) >= 4:
            pen = QPen(Qt.GlobalColor.red)
            pen.setWidth(3)
            painter.setPen(pen)
            points = self.coordenadas.get_points()
            painter.drawLine(int(points[0].x), int(points[0].y),
                           int(self.infinity_line[0].x), int(self.infinity_line[0].y))
            painter.drawLine(int(points[2].x), int(points[2].y),
                             int(self.infinity_line[0].x), int(self.infinity_line[0].y))

            painter.drawLine(int(points[0].x), int(points[0].y),
                           int(self.infinity_line[1].x), int(self.infinity_line[1].y))
            painter.drawLine(int(points[1].x), int(points[1].y),
                             int(self.infinity_line[1].x), int(self.infinity_line[1].y))

            pen = QPen(Qt.GlobalColor.darkBlue)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(int(self.infinity_line[0].x), int(self.infinity_line[0].y),
                             int(self.infinity_line[1].x), int(self.infinity_line[1].y))
        

# TODO: @María hacer que el tamaño de la ventana sea adaptable y la imagen se ajuste manteniendo su proporción
class ClickCaptureWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectificador de Imágenes")
        self.setWindowIcon(QIcon())

        # Título principal
        self.title = QLabel("Rectificador de Imágenes", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.title.setStyleSheet("margin: 20px;")

        # Área de clicks
        self.click_area = ClickArea(self)
        self.click_area.points_changed.connect(self.update_accept_button)

        # Contenedor para centrar
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)
        self.image_layout.addStretch()
        self.image_layout.addWidget(self.click_area)
        self.image_layout.addStretch()

        # Botones
        self.open_button = QPushButton("Abrir Imagen")
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setFont(QFont("Segoe UI", 14))

        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.accept_points)
        self.accept_button.setFont(QFont("Segoe UI", 14))

        # Contenedor para botones
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.open_button)
        self.buttons_layout.addWidget(self.accept_button)
        self.buttons_layout.addStretch()

        # Instrucciones
        self.instructions = QLabel(
            "Instrucciones:\n"
            "1. Abre una imagen\n"
            "2. Haz clic para marcar puntos (máx 4)\n"
            "3. Haz clic en un punto existente para eliminarlo\n"
            "4. Cuando tengas 4 puntos, haz clic en Aceptar"
        )
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setFont(QFont("Segoe UI", 12))
        self.instructions.setStyleSheet("margin: 10px;")

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.instructions)
        layout.addWidget(self.buttons_container)
        layout.addWidget(self.image_container, 1)
        self.setLayout(layout)

        self.apply_theme()
        self.showMaximized()

    def update_accept_button(self):
        self.accept_button.setEnabled(self.click_area.coordenadas.is_complete())

    def apply_theme(self):
        palette = self.palette()
        is_dark = palette.color(QPalette.Window).value() < 128

        if is_dark:
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: #FFFFFF; }
                QPushButton {
                    background-color: #333333; color: #FFFFFF;
                    border-radius: 10px; padding: 10px;
                }
                QPushButton:hover { background-color: #444444; }
                QPushButton:disabled { background-color: #222222; color: #888888; }
                QLabel { color: #FFFFFF; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #F0F0F0; color: #000000; }
                QPushButton {
                    background-color: #E0E0E0; color: #000000;
                    border-radius: 10px; padding: 10px;
                }
                QPushButton:hover { background-color: #CCCCCC; }
                QPushButton:disabled { background-color: #EEEEEE; color: #888888; }
                QLabel { color: #000000; }
            """)

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_dialog.exec():
            image_path = file_dialog.selectedFiles()[0]
            self.click_area.load_image(image_path)

    def accept_points(self):
        if self.click_area.coordenadas.is_complete():
            points = self.click_area.coordenadas.get_points()
            message = "\n".join([f"Punto {i + 1}: ({p.x:.1f}, {p.y:.1f})" for i, p in enumerate(points)])
            QMessageBox.information(self, "Puntos seleccionados", message)
            self.draw_lines() # DEBUG: Borrar después
        else:
            QMessageBox.warning(self, "Error", "Debes seleccionar exactamente 4 puntos")

    # DEBUG: Borrar después
    def draw_lines(self):
        points = self.click_area.coordenadas.get_points()
        infinity_line = calculate_infinity_line(points[0], points[1], points[2], points[3])
        self.click_area.set_infinity_line(infinity_line)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickCaptureWidget()
    window.show()
    sys.exit(app.exec())