from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from constants import GRAPHBOARD_SCALE

class ArrowDragPreview(QWidget):
    def __init__(self, arrow):
        super().__init__()

        pixmap = self.create_pixmap(arrow)
        
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(pixmap.height())
        self.label.setPixmap(pixmap)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.center = pixmap.rect().center() * GRAPHBOARD_SCALE
        
        self.color = arrow.color
        self.motion_type = arrow.motion_type
        self.quadrant = arrow.quadrant
        self.rotation_direction = arrow.rotation_direction
        self.turns = arrow.turns

        
        self.in_graphboard = False
        self.has_entered_graphboard_once = False

    def create_pixmap(self, dragged_arrow):
        new_svg_data = dragged_arrow.set_svg_color(dragged_arrow.svg_file, dragged_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)
        return pixmap
    
    def get_attr(self):
        return {
            'color': self.color,
            'motion_type': self.motion_type,
            'quadrant': self.quadrant,
            'rotation_direction': self.rotation_direction,
            'turns': self.turns
        }