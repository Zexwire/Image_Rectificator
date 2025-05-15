from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (QPainter, QPen, QMouseEvent, QPixmap)
from PySide6.QtWidgets import QWidget

from classes.points import Coordinates
from utils.infinity_line import calculate_vanish_points
from utils.projective_transform import find_sqr_points

# TODO: Añadir un botón de "clear points" o "borrar puntos" que elimine todos los puntos marcados
# TODO: ELiminar puntos dibujados innecesarios (cosas como el square points están para debuggear, deberán ser borrados para la versión final)
class ClickArea(QWidget):
    points_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.coordinates = Coordinates()
        self.image = None  # Store the scaled version
        self.setStyleSheet("background-color: #808080;")
        self.setMinimumSize(500, 500)
        self.point_radius = 10
        self.vanish_points = None
        self.square_points = None
        self.aspect_ratio = 0.0

    def set_aspect_ratio(self, ratio):
        self.aspect_ratio = ratio

    def load_image(self, image_path):
        self.image = QPixmap(image_path)
        self.scale_image()
        self.coordinates.clear()
        self.points_changed.emit()
        self.update()

    def scale_image(self):
        if not self.image:
            return

        # Get the current widget size
        available_width = self.width()
        available_height = self.height()

        # Scale the image to fit the widget while maintaining the aspect ratio
        self.image = self.image.scaled(
            available_width,
            available_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def get_image_position(self):
        if not self.image:
            return 0, 0
        return (self.width() - self.image.width()) // 2, (self.height() - self.image.height()) // 2

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.image:
            # Calculate the image position
            x_offset, y_offset = self.get_image_position()

            # Get click position relative to the image
            x = event.position().x() - x_offset
            y = event.position().y() - y_offset

            # Check if the click is within image bounds
            if (0 <= x <= self.image.width() and
                    0 <= y <= self.image.height()):
                if self.coordinates.remove_point_near(x, y, self.point_radius):
                    self.vanish_points = None
                    self.points_changed.emit()
                    self.update()
                elif not self.coordinates.is_complete():
                    self.coordinates.add_point(x, y, 1)
                    if self.coordinates.is_complete():
                        self.vanish_points = calculate_vanish_points(*self.coordinates.get_points())
                        if self.aspect_ratio:
                            self.square_points = find_sqr_points(self.coordinates, self.aspect_ratio)
                    self.points_changed.emit()
                    self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Fill the entire widget background with gray
        painter.fillRect(self.rect(), Qt.GlobalColor.gray)

        if self.image:
            # Calculate position to center the image
            x = (self.width() - self.image.width()) // 2
            y = (self.height() - self.image.height()) // 2
            painter.drawPixmap(x, y, self.image)

            # Adjust point coordinates based on image position
            if self.coordinates.points:
                colors = [Qt.GlobalColor.red, Qt.GlobalColor.green, Qt.GlobalColor.blue, Qt.GlobalColor.yellow]
                for i, point in enumerate(self.coordinates.points):
                    pen = QPen(colors[i])
                    pen.setWidth(8)
                    painter.setPen(pen)
                    painter.drawPoint(int(point.x + x), int(point.y + y))

            if self.vanish_points:
                pen = QPen(Qt.GlobalColor.red)
                pen.setWidth(3)
                painter.setPen(pen)
                for p in self.vanish_points:
                    if p:
                        painter.drawEllipse(int(p.x + x) - 5, int(p.y + y) - 5, 10, 10)
            if self.square_points:
                pen = QPen(Qt.GlobalColor.green)
                pen.setWidth(3)
                painter.setPen(pen)
                for p in self.square_points.get_points():
                    if p:
                        painter.drawEllipse(int(p.x + x) - 5, int(p.y + y) - 5, 10, 10)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_image()
        self.update()