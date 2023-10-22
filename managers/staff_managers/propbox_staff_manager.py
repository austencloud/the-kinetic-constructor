
from PyQt5.QtCore import QPointF
from objects.staff import Staff
from PyQt5.QtWidgets import QGraphicsItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from managers.staff_managers.staff_manager import Staff_Manager

class PropBox_Staff_Manager(Staff_Manager):
    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.propbox_view = None
        self.propbox_scene = None
        self.propbox_staffs = {}
        self.propbox_staff_locations = {}
    
    def init_propbox_staffs(self, propbox_view):
        propbox_scene = propbox_view.scene()
        
        # Define initial locations for propbox staffs
        self.propbox_staff_locations = {
            'N': QPointF(50, 100),
            'E': QPointF(100, 50),
            'S': QPointF(100, 100),
            'W': QPointF(100, 100)
        }
        
        # Create red and blue staffs in the propbox
        self.propbox_staffs = {}
        red_staff = Staff(propbox_scene, self.propbox_staff_locations['N'], 'red', 'N', 'propbox')
        blue_staff = Staff(propbox_scene, self.propbox_staff_locations['E'], 'blue', 'E', 'propbox')
        

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)

        self.propbox_staffs['red_staff'] = red_staff
        self.propbox_staffs['blue_staff'] = blue_staff
    
        
    def connect_propbox_view(self, propbox_view):
        self.propbox_view = propbox_view
