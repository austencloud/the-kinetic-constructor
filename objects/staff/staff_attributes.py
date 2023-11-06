from settings.string_constants import *


class StaffAttributes:
    STAFF_ATTRIBUTES = [COLOR, LOCATION, LAYER]

    def __init__(self, staff_manager):
        self.staff_manager = staff_manager

    def update_attributes_from_dict(self, staff, staff_dict):
        for attr in self.STAFF_ATTRIBUTES:
            value = staff_dict.get(attr)
            setattr(staff, attr, value)

    def get_attributes(self, staff):
        return {attr: getattr(staff, attr) for attr in self.STAFF_ATTRIBUTES}

    def create_staff_dict_from_arrow(self, arrow):
        staff_dict = {COLOR: arrow.color, LOCATION: arrow.end_location, LAYER: 1}
        return staff_dict

    def update_attributes_from_arrow(self, arrow):
        staff = arrow.staff
        updated_staff_dict = {
            COLOR: arrow.color,
            LOCATION: arrow.end_location,
            LAYER: 1,
        }
        staff.attributes.update_attributes_from_dict(staff, updated_staff_dict)
        staff.update_appearance()
        staff.setPos(arrow.scene.grid.handpoints[staff.location])
