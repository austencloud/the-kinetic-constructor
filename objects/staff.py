from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from constants import GRAPHBOARD_SCALE, PICTOGRAPH_SCALE, STAFF_WIDTH, STAFF_LENGTH
class Staff(QGraphicsSvgItem):
    SCALE_MAP = {
        'graphboard': GRAPHBOARD_SCALE,
        'pictograph': PICTOGRAPH_SCALE,
        'default': GRAPHBOARD_SCALE
    }
    COLOR_MAP = {
        "red": "#ed1c24",
        "blue": "#2E3192"
    }
    
    def __init__(self, scene, xy_location, color, location=None, context=None):
        super().__init__()
        image_file = f'images/staffs/staff.svg'
        self.xy_location = xy_location 
        self.renderer = QSvgRenderer(image_file)
        self.setSharedRenderer(self.renderer)
        scene.addItem(self)
        self.arrow = None
        self.setVisible(True)
        self.setTransformOriginPoint(0, 0)
        self.svg_file = image_file
        self.set_color(color)
        self.location = location
        scale = self.SCALE_MAP.get(context, self.SCALE_MAP['default'])
        self.set_initial_position(location, scale)

        self.color = color
        self.context = context
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.setScale(scale)  


    def set_initial_position(self, location, scale):
        x_offset, y_offset = 0, 0

        if location in ['N', 'S']:
            self.axis = 'vertical'
            self.setRotation(90)
            x_offset = (STAFF_WIDTH / 2) * scale
            y_offset = -(STAFF_LENGTH / 2) * scale
        elif location in ['E', 'W']:
            self.axis = 'horizontal'
            x_offset = -(STAFF_LENGTH / 2) * scale
            y_offset = -(STAFF_WIDTH / 2) * scale

        self.setPos(self.xy_location.x() + x_offset, self.xy_location.y() + y_offset)
    def mousePressEvent(self, event):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            x_offset, y_offset = self.get_staff_center()
            self.setPos(event.scenePos().x() + x_offset, event.scenePos().y() + y_offset)
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # Add your snapping logic here
        super().mouseReleaseEvent(event)
    
    def get_staff_center(self):
        if self.axis == 'vertical':
            return (STAFF_WIDTH / 2) * GRAPHBOARD_SCALE, -(STAFF_LENGTH / 2) * GRAPHBOARD_SCALE
        elif self.axis == 'horizontal':
            return -(STAFF_LENGTH / 2) * GRAPHBOARD_SCALE, -(STAFF_WIDTH / 2) * GRAPHBOARD_SCALE
        return 0, 0

    def set_color(self, new_color):
        hex_color = self.COLOR_MAP.get(new_color, new_color)
        with open(self.svg_file, 'r') as f:
            svg_data = f.read()
            
        old_colors = ["#ed1c24", "#2E3192"]
        for old_color in old_colors:
            svg_data = svg_data.replace(old_color, hex_color)
            
        self.renderer.load(svg_data.encode('utf-8'))
        self.color = hex_color


