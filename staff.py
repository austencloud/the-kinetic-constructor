from PyQt5.QtCore import QPointF, pyqtSignal, QObject
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsItem
from arrow import Arrow
from settings import Settings
from constants import STAFF_WIDTH, STAFF_LENGTH, RED, BLUE

SCALE_FACTOR = Settings.SCALE_FACTOR

class Staff(QGraphicsSvgItem):

    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None, initial_visibility=True):
        super().__init__()
        self.element_id = element_id
        self.position = position 
        self.renderer = QSvgRenderer(staff_svg_file)
        self.setSharedRenderer(self.renderer)
        self.setElementId(self.element_id)
        scene.addItem(self)
        self.setVisible(initial_visibility)
        self.type = "staff"
        self.scene = scene
        self.setPos(position)
        self.arrow = None
        self.setVisible(True)
        rect = self.boundingRect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.setPos(position)
        self.svg_file = staff_svg_file
        self.color = color

        self.is_static = False
        
    def update_attributes(self, new_attributes):
        self.element_id = new_attributes.get('element_id', self.element_id)
        self.position = new_attributes.get('position', self.position)
        self.svg_file = new_attributes.get('svg_file', self.svg_file)
        self.color = new_attributes.get('color', self.color)

    def set_static(self, is_static):
        self.is_static = is_static

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)

    def set_arrow(self, arrow):
        self.arrow = arrow
        
    def isVisible(self):
        return super().isVisible()

class Graphboard_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)
        print(f"=== Creating Graphboard_Staff: {element_id} ===")

class Beta_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file, initial_visibility=False)

class PropBox_Staff(Staff):
    def __init__(self, element_id, scene, position, color=None, staff_svg_file=None):
        super().__init__(element_id, scene, position, color, staff_svg_file)
   