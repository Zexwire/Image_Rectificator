from PySide6.QtCore import QStandardPaths

from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QMessageBox, QFileDialog, QHBoxLayout, QMainWindow)

from utils.projective_transform import *
from widgets.buttons import PrimaryButton, SecondaryButton
from widgets.click_area import ClickArea
from widgets.menu import Menu, AspectRatioWidget

class ApplicationWindow(QMainWindow):
    ASPECT_RATIO = 0.0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectificador de Imágenes")

        main_layout = QHBoxLayout()

        menu_container_widget = QWidget()
        menu_container_widget.setFixedWidth(500)

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(5, 5, 5, 5)

        self.open_image_button = SecondaryButton("Abrir Imagen")
        self.open_image_button.clicked.connect(self.open_image)

        self.transform_button = PrimaryButton("Rectificar")
        self.transform_button.setEnabled(False)
        self.transform_button.clicked.connect(self.transform_image)

        self.aspect_ratio_widget = AspectRatioWidget()
        self.aspect_ratio_widget.aspect_ratio_changed.connect(self.update_transform_button)

        menu_layout.addWidget(Menu(self.aspect_ratio_widget))
        menu_layout.addStretch()
        menu_layout.addWidget(self.open_image_button)
        menu_layout.addWidget(self.transform_button)

        menu_container_widget.setLayout(menu_layout)

        self.click_area = ClickArea(self)
        self.click_area.points_changed.connect(self.update_transform_button)

        main_layout.addWidget(menu_container_widget)
        main_layout.addWidget(self.click_area)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_image(self):
        pictures_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        file_dialog = QFileDialog(self, "Seleccionar imagen", pictures_path)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if file_dialog.exec():
            image_path = file_dialog.selectedFiles()[0]
            self.click_area.load_image(image_path)
    def update_transform_button(self):
        self.ASPECT_RATIO = self.aspect_ratio_widget.get_aspect_ratio()
        self.click_area.set_aspect_ratio(self.ASPECT_RATIO)
        enabled = self.click_area.coordinates.is_complete() and self.ASPECT_RATIO != 0
        self.transform_button.setEnabled(enabled)
    def transform_image(self):
        try:
            if not self.click_area.square_points and self.click_area.aspect_ratio:
                self.click_area.square_points = find_sqr_points(self.click_area.coordinates, self.click_area.aspect_ratio)
            H = calculate_homography(self.click_area.square_points, self.click_area.width() if self.click_area.width() < self.click_area.height() else self.click_area.height())
            self.click_area.image = warp_perspective_qpixmap(self.click_area.image, H, (self.click_area.width(),self.click_area.height()))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al rectificar:\n{str(e)}")