import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                              QLabel, QMessageBox, QFrame, QFileDialog, QHBoxLayout)
from PySide6.QtGui import (QPainter, QPen, QMouseEvent, QPixmap, QFont, 
                          QPalette, QIcon, QImage)
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QScrollArea

from classes import Coordenadas, Punto
from projective_transform import apply_projective_transform
from infinity_line import calculate_infinity_line

def numpy_to_pixmap(image: np.ndarray) -> QPixmap:
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)

class ClickArea(QFrame):
    points_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.coordenadas = Coordenadas()
        self.image = None
        self.setStyleSheet("background-color: #808080;")
        self.setMinimumSize(800, 800)
        self.point_radius = 10
        self.infinity_line = None

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

            if self.coordenadas.remove_point_near(x, y, self.point_radius):
                self.infinity_line = None
                self.points_changed.emit()
                self.update()
            elif not self.coordenadas.is_complete():
                self.coordenadas.add_point(x, y)
                if self.coordenadas.is_complete():
                    self.infinity_line = calculate_infinity_line(*self.coordenadas.get_points())
                self.points_changed.emit()
                self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        if self.image:
            painter.drawPixmap(0, 0, self.image)

        if self.coordenadas.points:
            colors = [Qt.GlobalColor.red, Qt.GlobalColor.green, Qt.GlobalColor.blue, Qt.GlobalColor.yellow]
            for i, point in enumerate(self.coordenadas.points):
                pen = QPen(colors[i])
                pen.setWidth(8)
                painter.setPen(pen)
                painter.drawPoint(int(point.x), int(point.y))

        if self.infinity_line:
            pen = QPen(Qt.GlobalColor.red)
            pen.setWidth(3)
            painter.setPen(pen)
            for p in self.infinity_line:
                if p:
                    painter.drawEllipse(int(p.x)-5, int(p.y)-5, 10, 10)

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
            try:
                # Convertir QPixmap a numpy array
                qimage = self.click_area.image.toImage().convertToFormat(QImage.Format_RGB888)
                width, height = qimage.width(), qimage.height()
                ptr = qimage.constBits()
                arr = np.array(ptr).reshape(height, width, 3)
                
                # Rectificar imagen
                rectified = apply_projective_transform(arr, self.click_area.coordenadas.get_points())
                
                # Crear o actualizar ventana de resultados
                if not hasattr(self, 'result_window'):
                    self.result_window = QWidget()
                    self.result_window.setWindowTitle("Imagen Rectificada")
                    self.result_window.setMinimumSize(400, 400)  # Tamaño mínimo
                    self.result_window.resize(600, 600)          # Tamaño inicial
                    
                    # Layout principal
                    self.result_layout = QVBoxLayout(self.result_window)
                    
                    # Área de scroll (para imágenes grandes)
                    self.scroll_area = QScrollArea()
                    self.scroll_area.setWidgetResizable(True)
                    
                    # Label para la imagen (dentro del scroll)
                    self.result_label = QLabel()
                    self.result_label.setAlignment(Qt.AlignCenter)
                    self.scroll_area.setWidget(self.result_label)
                    
                    # Botón para guardar
                    self.save_button = QPushButton("Guardar Imagen")
                    self.save_button.clicked.connect(lambda: self.save_image(self.result_label.pixmap()))
                    
                    # Añadir widgets al layout
                    self.result_layout.addWidget(self.scroll_area)
                    self.result_layout.addWidget(self.save_button)
                
                # Mostrar la imagen rectificada
                height, width, _ = rectified.shape
                bytes_per_line = 3 * width
                qimage = QImage(rectified.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.original_pixmap = QPixmap.fromImage(qimage)  # Guardamos la imagen original
                
                # Escalar la imagen al tamaño actual del scroll area
                self.update_image_size()
                
                # Conectar el redimensionamiento de la ventana
                self.result_window.resizeEvent = lambda event: self.update_image_size()
                
                self.result_window.show()
                self.result_window.raise_()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al rectificar:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Se necesitan exactamente 4 puntos")

    def update_image_size(self):
        """Actualiza el tamaño de la imagen cuando se redimensiona la ventana"""
        if hasattr(self, 'result_window') and hasattr(self, 'original_pixmap'):
            # Calcula el nuevo tamaño (dejando espacio para el botón y márgenes)
            new_width = self.scroll_area.width() - 20
            if new_width > 0:
                scaled_pixmap = self.original_pixmap.scaledToWidth(
                    new_width, 
                    Qt.SmoothTransformation
                )
                self.result_label.setPixmap(scaled_pixmap)

    def save_image(self, pixmap):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar Imagen Rectificada", 
            "", 
            "Imágenes (*.png *.jpg *.bmp)"
        )
        if file_path:
            pixmap.save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickCaptureWidget()
    window.show()
    sys.exit(app.exec())