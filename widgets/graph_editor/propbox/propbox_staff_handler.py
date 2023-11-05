from PyQt6.QtCore import QPointF

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.staff.staff_handler import StaffManager
from settings.string_constants import *


class PropboxStaffHandler(StaffManager):
    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.propbox = None

    def init_propbox_staffs(self, propbox):

        self.propbox_staff_locations = {
            NORTH: QPointF(50, 100),
            EAST: QPointF(100, 50),
            SOUTH: QPointF(100, 100),
            WEST: QPointF(100, 100),
        }

        red_propbox_staff = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        blue_propbox_staff = {
            COLOR: BLUE,
            LOCATION: NORTH,
            LAYER: 1,
        }

        # Create red and blue staffs in the propbox
        red_staff = self.factory.create_staff(propbox, red_propbox_staff)
        blue_staff = self.factory.create_staff(propbox, blue_propbox_staff)

        red_staff.setPos(self.propbox_staff_locations[EAST])
        blue_staff.setPos(self.propbox_staff_locations[NORTH])

        propbox.addItem(red_staff)
        propbox.addItem(blue_staff)

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
