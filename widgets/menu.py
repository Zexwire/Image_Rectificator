from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                               QLabel, QFrame, QHBoxLayout, QLineEdit)

from utils.dark_mode import is_dark_mode


class Menu(QWidget):
    def __init__(self, aspect_ratio_widget):
        super().__init__()
        layout = QVBoxLayout()

        # Cabecera con logo y título ---
        header_widget = QWidget()
        header_layout = QHBoxLayout()

        # Logo adaptado a tema claro/oscuro
        logo_label = QLabel()
        logo_path = "assets/Logo_Dark.png" if is_dark_mode() else "assets/Logo_Light.png"
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))

        # Título "QuadFix"
        title_label = QLabel("QuadFix")
        title_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            padding-left: 10px;
        """)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()  # Para alinear a la izquierda
        header_widget.setLayout(header_layout)

        instructions_widget = CollapsibleSection(
            "Instrucciones")

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Raised)

        layout.addWidget(header_widget)
        layout.addWidget(instructions_widget)
        layout.addWidget(line)
        layout.addWidget(aspect_ratio_widget)

        self.setLayout(layout)

class CollapsibleSection(QWidget):
    def __init__(self, title: str):
        super().__init__()

        self.toggle_button = QPushButton(f"▸ {title}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_content)
        self.toggle_button.setStyleSheet("""
                    QPushButton {
                        background: none;
                        border: none;
                        text-align: left;
                        font-weight: bold;
                        font-size: 15pt;
                        padding: 4px;
                    }
                    QPushButton:hover {
                        background: rgba(36, 147, 237, 0.15);
                    }
                """)

        content_area = QWidget()
        content_area.setVisible(False)
        self.content_area = content_area

        content_label = QLabel("1. Haga clic en 'Abrir Imagen' y seleccione una imagen.\n"
            "2. Haga clic sobre la imagen para marcar las esquinas del cuadrado o rectángulo a rectificar. *\n"
            "3. Si se equivoca, haga clic en la esquina que desee eliminar.\n"
            "4. Cuando las 4 esquinas estén marcadas, haga clic en 'Rectificar'.")
        content_label.setWordWrap(True)
        content_label.setStyleSheet("padding-left: 20px; background-color: rgba(128, 128, 128, 0.0);")

        corners_instructions_label = QLabel("* El orden de las esquinas en la imagen rectificada será el siguiente: \n")
        corners_instructions_label.setWordWrap(True)
        corners_instructions_label.setStyleSheet("padding-left: 10px; background-color: rgba(128, 128, 128, 0.0);")
        corners_instructions_image = QLabel()
        corners_instructions_image.setPixmap(QPixmap("assets/corners-instructions.png"))
        corners_instructions_image.setScaledContents(True)
        corners_instructions_image.setFixedSize(100, 100)


        layout = QVBoxLayout()
        layout.addWidget(content_label)
        layout.addWidget(corners_instructions_label)
        layout.addWidget(corners_instructions_image, alignment=Qt.AlignmentFlag.AlignCenter)
        content_area.setLayout(layout)
        content_area.setStyleSheet("background-color: rgba(128, 128, 128, 0.2); padding: 10px; border-radius: 10px;")

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)

    def toggle_content(self):
        is_expanded = self.toggle_button.isChecked()
        self.content_area.setVisible(is_expanded)
        if is_expanded:
            self.toggle_button.setText(self.toggle_button.text().replace("▸ ", "▾ "))
        else:
            self.toggle_button.setText(self.toggle_button.text().replace("▾ ", "▸ "))

from PySide6.QtCore import Signal

class AspectRatioWidget(QWidget):
    aspect_ratio_changed = Signal(float)

    def __init__(self):
        super().__init__()
        self.aspect_ratio = 0.0

        main_layout = QVBoxLayout()
        ratio_input_layout = QHBoxLayout()

        ratio_input_label = QLabel("Razón: ")
        ratio_input_label.setStyleSheet("font-weight: 650; font-size: 12pt;")

        ratio_input = QLineEdit()
        ratio_input.setPlaceholderText("Introduzca la razón de su figura (e.g. 1.0)")
        ratio_input.textChanged.connect(self.on_ratio_changed)

        ratio_input_layout.addWidget(ratio_input_label)
        ratio_input_layout.addWidget(ratio_input)

        instructions = QLabel("Para calcular la razón, debe dividir ALTO / ANCHO de su figura. Por ejemplo:\n"
                              "    -   En caso de ser un cuadrado, la razón será 1.0.\n"
                              "    -   En caso de ser un folio DinA4 vertical, la razón será 1.4142135.")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("""
            background-color: rgba(128, 128, 128, 0.2);
            padding: 10px;
            border-radius: 10px;
        """)

        main_layout.addLayout(ratio_input_layout)
        main_layout.addWidget(instructions)

        self.setLayout(main_layout)

    def on_ratio_changed(self, text):
        try:
            self.aspect_ratio = float(text)
        except ValueError:
            self.aspect_ratio = 0.0

        self.aspect_ratio_changed.emit(self.aspect_ratio)

    def get_aspect_ratio(self):
        return self.aspect_ratio
