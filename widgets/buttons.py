from PySide6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    button_style = """
        QPushButton {
            background-color: rgba(36, 147, 237, 0.8);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        QPushButton:pressed {
            background-color: rgba(36, 147, 237, 1);
        }
        QPushButton:disabled {
            background-color: rgba(100, 150, 200, 0.3);
            color: rgba(255, 255, 255, 0.5);
        }
    """

    def __init__(self, text: str):
        super().__init__(text)
        self.setStyleSheet(self.button_style)

from PySide6.QtWidgets import QPushButton


class SecondaryButton(QPushButton):
    button_style = """
        QPushButton {
            background-color: rgba(138, 138, 138, 0.2);
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        QPushButton:pressed {
            background-color: rgba(138, 138, 138, 0.4);
        }
    """

    def __init__(self, text: str):
        super().__init__(text)
        self.setStyleSheet(self.button_style)