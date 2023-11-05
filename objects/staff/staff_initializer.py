from settings.string_constants import *


class StaffInitializer:
    def __init__(self, staff_factory):
        self.staff_factory = staff_factory

    def init_staffs(self, view):
        scene = view.scene()
        staffs = []

        red_staff_dict = {
            COLOR: RED,
            LOCATION: NORTH,
            LAYER: 1,
        }
        blue_staff_dict = {
            COLOR: BLUE,
            LOCATION: SOUTH,
            LAYER: 1,
        }

        red_staff = self.staff_factory.create_staff(scene, red_staff_dict)
        blue_staff = self.staff_factory.create_staff(scene, blue_staff_dict)
        scene.addItem(red_staff)
        scene.addItem(blue_staff)

        staffs.append(red_staff)
        staffs.append(blue_staff)

        view.staffs = staffs
        view.staff_handler.visibility_manager.hide_all_staffs(view.scene())
