from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from constants import GRAPHBOARD_SCALE
class ArrowDragPreview(QWidget):
    def __init__(self, pixmap, arrow):
        super().__init__()
        # Debugging: Set a background color to check visibility
        self.setStyleSheet("background-color: transparent;")
        
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(pixmap.height())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.center = pixmap.rect().center() * GRAPHBOARD_SCALE

        self.rotation_direction = arrow.rotation_direction
        self.motion_type = arrow.motion_type
        
    def setPixmap(self, pixmap):
        self.label.setPixmap(pixmap)

