from PyQt6.QtCore import QPointF
from objects.staff.staff import Staff
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.staff.staff_handler import StaffManager
from settings.string_constants import COLOR, RED, BLUE


class PropboxStaffHandler(StaffManager):
    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.propbox_view = None

    def init_propbox_staffs(self, propbox_view):
        propbox_scene = propbox_view.propbox_scene

        self.propbox_staff_locations = {
            "n": QPointF(50, 100),
            "e": QPointF(100, 50),
            "s": QPointF(100, 100),
            "w": QPointF(100, 100),
        }

        red_propbox_staff = {
            COLOR: RED,
            "location": "e",
            "layer": 1,
        }

        blue_propbox_staff = {
            COLOR: BLUE,
            "location": "n",
            "layer": 1,
        }

        # Create red and blue staffs in the propbox
        red_staff = self.factory.create_staff(propbox_scene, red_propbox_staff)
        blue_staff = self.factory.create_staff(propbox_scene, blue_propbox_staff)

        red_staff.setPos(self.propbox_staff_locations["e"])
        blue_staff.setPos(self.propbox_staff_locations["n"])

        propbox_scene.addItem(red_staff)
        propbox_scene.addItem(blue_staff)

        red_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        blue_staff.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
