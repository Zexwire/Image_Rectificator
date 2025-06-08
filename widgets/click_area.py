from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import (QPainter, QPen, QMouseEvent, QPixmap)
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication

from classes.points import Coordinates
from utils.infinity_line import calculate_vanish_points


class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.hide()

        # Make sure overlay covers the entire parent
        self.resize_to_parent()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.loading_label = QLabel("Cargando...")

        layout.addWidget(self.loading_label)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); font-family: 'Segoe UI';"
                 "font-size: 20pt;"
                 "text-align: left;")

    def resize_to_parent(self):
        if self.parent():
            self.setGeometry(self.parent().rect())

    def show_loading(self, show: bool):
        if show:
            self.resize_to_parent()
            self.raise_()
            self.show()
            QApplication.processEvents()
        else:
            self.hide()

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
                    self.points_changed.emit()
                    self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Fill the entire widget background with gray
        painter.fillRect(self.rect(), Qt.GlobalColor.gray)

        if self.image:
            # Calculate position to center the image
            x, y = self.get_image_position()
            painter.drawPixmap(x, y, self.image)

            # Adjust point coordinates based on image position
            if self.coordinates.get_points():
                for i, point in self.coordinates.points.items():
                    pen = QPen(Qt.GlobalColor.red)
                    pen.setWidth(8)
                    painter.setPen(pen)
                    painter.drawPoint(int(point.x + x), int(point.y + y))

                    # Configure font for numbers
                    font = painter.font()
                    font.setPointSize(14)
                    font.setBold(True)
                    painter.setFont(font)

                    # Get text dimensions for background
                    text = str(i + 1)
                    text_width = painter.fontMetrics().horizontalAdvance(text)
                    text_height = painter.fontMetrics().height()

                    # Draw semi-transparent background
                    painter.setOpacity(0.5)  # Set transparency (0.0 fully transparent, 1.0 fully opaque)
                    painter.fillRect(
                        int(point.x + x + 10 - 2),  # X position (slight padding before text)
                        int(point.y + y - 10 - text_height + 2),  # Y position
                        text_width + 4,  # Width with padding
                        text_height + 2,  # Height with padding
                        Qt.GlobalColor.white
                    )

                    # Reset opacity and draw the number
                    painter.setOpacity(1.0)
                    painter.setPen(QPen(Qt.GlobalColor.black))  # Black text for better contrast on white background
                    painter.drawText(
                        int(point.x + x + 10),
                        int(point.y + y - 10),
                        text
                    )
            if self.vanish_points:
                    pen = QPen(Qt.GlobalColor.red)
                    pen.setWidth(3)
                    painter.setPen(pen)
                    for p in self.vanish_points:
                        if p:
                            painter.drawEllipse(int(p.x + x) - 5, int(p.y + y) - 5, 10, 10)

    def clear_points(self):
        self.coordinates.clear()
        self.vanish_points = None
        self.points_changed.emit()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scale_image()
        self.update()