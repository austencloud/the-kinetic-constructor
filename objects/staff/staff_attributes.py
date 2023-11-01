class StaffAttributes:
    STAFF_ATTRIBUTES = ["color", "location", "layer"]

    def __init__(self, staff, staff_dict):
        self.update_attributes_from_dict(staff, staff_dict)


    def update_attributes_from_dict(self, staff, staff_dict):
        for attr in self.STAFF_ATTRIBUTES:
            value = staff_dict.get(attr)
            setattr(staff, attr, value)

    def get_attributes(self, staff):
        return {attr: getattr(staff, attr) for attr in self.STAFF_ATTRIBUTES}

    def create_staff_dict(self, color, location, layer):
        staff_dict = {"color": color, "location": location, "layer": layer}
        return staff_dict

    def update_attributes_from_arrow(self, arrow):
        staff = arrow.staff
        updated_staff_dict = {
            "color": arrow.color,
            "location": arrow.end_location,
            "layer": 1,
        }
        staff.attributes.update_attributes_from_dict(staff, updated_staff_dict)
        staff.update_appearance()
        staff.setPos(arrow.view.staff_handler.staff_xy_locations[staff.location])
