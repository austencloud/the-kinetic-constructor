from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class PreviewArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.preview_label = QLabel("Select a thumbnail to display it here.")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.preview_label)
        self.edit_sequence_button = QPushButton("Edit Sequence")
        self.layout.addWidget(self.edit_sequence_button)

    def set_preview_pixmap(self, pixmap):
        self.preview_label.setPixmap(pixmap)

    def set_edit_sequence_callback(self, callback):
        self.edit_sequence_button.clicked.connect(callback)
