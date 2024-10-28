from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption


class CueLabelEdit(QTextEdit):
    def __init__(self, max_width):
        super().__init__()
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMaximumWidth(max_width)
        self.setFixedWidth(max_width)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.MinimumExpanding
        )

    def keyPressEvent(self, event):
        """Capture Enter key to trigger acceptance if desired."""
        if event.key() == Qt.Key.Key_Return:
            self.clearFocus()  # Or custom behavior
        else:
            super().keyPressEvent(event)
