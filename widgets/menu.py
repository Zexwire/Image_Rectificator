from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                               QLabel, QFrame, QHBoxLayout, QLineEdit)


class Menu(QWidget):
    def __init__(self, aspect_ratio_widget):
        super().__init__()
        layout = QVBoxLayout()

        instructions_widget = CollapsibleSection(
            "Instrucciones",
            "1. Seleccione una imagen\n"
            "2. Haga clic sobre la imagen para marcar esquinas (máx 4)\n"
            "3. Si se equivoca, haga clic en el punto existente que desee eliminar\n"
            "4. Cuando las 4 esquinas estén marcadas, haga click en Aceptar")

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Raised)

        layout.addWidget(instructions_widget)
        layout.addWidget(line)
        layout.addWidget(aspect_ratio_widget)

        self.setLayout(layout)

class CollapsibleSection(QWidget):
    def __init__(self, title: str, content: str):
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

        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("padding-left: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(content_label)
        content_area.setLayout(layout)

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
                              "    -   En caso de ser un folio DinA4, la razón será 1.4142135 (en vertical) o 0.7071067 (en horizontal).")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("opacity: 0.1;")

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
