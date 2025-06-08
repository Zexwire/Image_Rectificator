from PySide6.QtCore import QStandardPaths

from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QMessageBox, QFileDialog, QHBoxLayout, QMainWindow)

from utils.projective_transform import *
from widgets.buttons import PrimaryButton, SecondaryButton
from widgets.click_area import ClickArea, OverlayWidget
from widgets.menu import Menu, AspectRatioWidget

import traceback

class ApplicationWindow(QMainWindow):
    ASPECT_RATIO = 0.0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectificador de Imágenes")

        main_layout = QHBoxLayout()

        self.click_area = ClickArea(self)
        self.click_area.points_changed.connect(self.update_transform_button)

        menu_container_widget = QWidget()
        menu_container_widget.setFixedWidth(500)

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(5, 5, 5, 50)

        self.open_image_button = SecondaryButton("Abrir Imagen")
        self.open_image_button.clicked.connect(self.open_image)

        self.clear_points_button = SecondaryButton("Limpiar Puntos")
        self.clear_points_button.setEnabled(False)
        self.clear_points_button.clicked.connect(self.click_area.clear_points)

        self.transform_button = PrimaryButton("Rectificar")
        self.transform_button.setEnabled(False)
        self.transform_button.clicked.connect(self.transform_image)

        self.download_button = PrimaryButton("Descargar Imagen")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.save_image)

        self.aspect_ratio_widget = AspectRatioWidget()
        self.aspect_ratio_widget.aspect_ratio_changed.connect(self.update_transform_button)

        menu_layout.addWidget(Menu(self.aspect_ratio_widget))
        menu_layout.addStretch()
        menu_layout.addWidget(self.open_image_button)
        menu_layout.addWidget(self.clear_points_button)
        menu_layout.addWidget(self.transform_button)
        menu_layout.addWidget(self.download_button) 

        menu_container_widget.setLayout(menu_layout)

        click_area_container = QWidget()
        click_area_layout = QVBoxLayout(click_area_container)
        click_area_layout.setContentsMargins(0, 0, 0, 0)
        click_area_layout.addWidget(self.click_area)

        self.overlay_loading_widget = OverlayWidget(self.click_area)

        main_layout.addWidget(menu_container_widget)
        main_layout.addWidget(click_area_container)

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
            self.download_button.setEnabled(False)
    def update_transform_button(self):
        self.ASPECT_RATIO = self.aspect_ratio_widget.get_aspect_ratio()
        self.click_area.set_aspect_ratio(self.ASPECT_RATIO)
        enabled = self.click_area.coordinates.is_complete() and self.ASPECT_RATIO != 0
        self.transform_button.setEnabled(enabled)
        self.clear_points_button.setEnabled(len(self.click_area.coordinates.points) > 0)
    def transform_image(self):
        try:
            self.overlay_loading_widget.show_loading(True)

            H = calculate_homography(self.click_area.coordinates, self.click_area.width() if self.click_area.width() < self.click_area.height() else self.click_area.height(), self.click_area.aspect_ratio)
            self.click_area.image = warp_perspective_qpixmap(self.click_area.image, H, (self.click_area.width(),self.click_area.height()))

            self.download_button.setEnabled(True)
            
            self.overlay_loading_widget.show_loading(False)
            self.click_area.clear_points()
        except Exception as e:
            self.overlay_loading_widget.show_loading(False)
            tb = traceback.format_exc()
            QMessageBox.critical(self, "Error", f"Error al rectificar:\n{str(e)}\n\n{tb}")

    def save_image(self):
        if not self.click_area.image:
            return

        # Obtener la ruta para guardar la imagen
        pictures_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar imagen rectificada",
            pictures_path + "/imagen_rectificada.png",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            self.click_area.image.save(file_path)
            QMessageBox.information(self, "Éxito", "Imagen guardada correctamente")