from PyQt6.QtWidgets import QPushButton


class LetterBookLetterButtonStyler:
    DEFAULT_STYLE = """
        QPushButton {
            background-color: white;
            border: 1px solid black;
            border-radius: 0px;
            padding: 0px;
        }
        QPushButton:hover {
            background-color: #e6f0ff;
        }
        QPushButton:pressed {
            background-color: #cce0ff;
        }
    """

    @staticmethod
    def apply_default_style(button: QPushButton):
        button.setStyleSheet(LetterBookLetterButtonStyler.DEFAULT_STYLE)
