from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from settings import GRAPHBOARD_SCALE
class Staff(QGraphicsSvgItem):
    def __init__(self, scene, xy_location, axis, color, location=None, context=None):
        super().__init__()
        image_file = f'images/staffs/staff.svg'
        self.xy_location = xy_location 
        self.renderer = QSvgRenderer(image_file)
        self.setSharedRenderer(self.renderer)
        scene.addItem(self)
        self.scene = scene
        self.arrow = None
        self.setVisible(True)
        rect = self.boundingRect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.setPos(xy_location.x(), xy_location.y())
        self.svg_file = image_file
        self.color = color
        self.axis = axis
        self.location = location
        self.color = color
        self.context = context
        self.setScale(GRAPHBOARD_SCALE)
        #make them selectable
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def mousePressEvent(self, event):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButtons.LeftButton:
            self.setPos(event.scenePos() - self.boundingRect().center())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # Add your snapping logic here
        super().mouseReleaseEvent(event)
        
    def set_element(self, element_id, color):
        self.setElementId(element_id)
        self.color = color
        # Add any other attributes you want to change        

    def set_element(self, element_id, color):
        self.setElementId(element_id)
        self.color = color
        if color:
            self.set_color(color)

    def set_color(self, color):
        color = QColor(color)
        self.setBrush(color)

    def hide(self):
        self.setVisible(False)

    def set_arrow(self, arrow):
        self.arrow = arrow
        
    def isVisible(self):
        return super().isVisible()
    
    def set_arrow(self, arrow):
        self.arrow = arrow

    def get_arrow(self):
        return self.arrow