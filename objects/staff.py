from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import Qt
from constants import GRAPHBOARD_SCALE, PICTOGRAPH_SCALE, STAFF_WIDTH, STAFF_LENGTH, COLOR_MAP

''' 
staff_dict = {
            "color": "red",
            "location": "e",
            "layer": 1,
        }
        
'''
class Staff(QGraphicsSvgItem):
    def __init__(self, scene, staff_dict):
        super().__init__()
        self.svg_file = 'images/staffs/staff.svg'
        self.scene = scene
        self.view = scene.views()[0]
        self.initialize_dict_attributes(staff_dict)
        self.initialize_app_attributes(scene)

    def initialize_dict_attributes(self, staff_dict):
        self.color = staff_dict.get('color')
        self.location = staff_dict.get('location')
        self.layer = staff_dict.get('layer')
        
        self.set_axis(staff_dict)
        self.set_rotation()

    def set_axis(self, staff_dict):
        axis_switch = {
            1: {'horizontal': ['w', 'e'], 'vertical': ['n', 's']},
            2: {'horizontal': ['n', 's'], 'vertical': ['w', 'e']}
        }

        self.axis = next(
            axis for axis, locations in axis_switch.get(self.layer, {}).items()
            if staff_dict.get('location') in locations
        )

    def initialize_app_attributes(self, scene):
        self.renderer = QSvgRenderer(self.svg_file)
        self.setSharedRenderer(self.renderer)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        
        self.setScale(self.view.view_scale)
        self.set_color(self.color)
        scene.addItem(self)


    def get_staff_center(self, scale):
        if self.axis == 'vertical':
            return (STAFF_WIDTH / 2) * scale, -(STAFF_LENGTH / 2) * scale
        return -(STAFF_LENGTH / 2) * scale, -(STAFF_WIDTH / 2) * scale

    def set_color(self, new_color):
        hex_color = COLOR_MAP.get(new_color, new_color)
        with open(self.svg_file, 'r') as f:
            svg_data = f.read().replace("#ed1c24", hex_color).replace("#2E3192", hex_color)
        self.renderer.load(svg_data.encode('utf-8'))
        self.color = hex_color

    def rotate_staff(self):
        if self.axis == 'vertical':
            self.axis = 'horizontal'
        else:
            self.axis = 'vertical'
        self.set_rotation()
        
    def set_rotation(self):
        if self.axis == 'vertical':
            self.current_position = self.pos()
            self.setTransformOriginPoint(self.boundingRect().center())
            self.setRotation(90)

    
        else:
            self.setRotation(0)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            x_offset, y_offset = self.get_staff_center(self.view.view_scale)
            self.setPos(event.scenePos().x() + x_offset, event.scenePos().y() + y_offset)
        super().mouseMoveEvent(event)
