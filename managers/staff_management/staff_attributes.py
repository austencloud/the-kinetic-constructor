class StaffAttributes:
    STAFF_ATTRIBUTES = ['color', 'location', 'layer']
    
    def __init__(self, staff, staff_dict):    
        self.update_attributes_from_dict(staff, staff_dict)

    def update_attributes_from_dict(self, staff, staff_dict):
        for attr in self.STAFF_ATTRIBUTES:
            value = staff_dict.get(attr)
            setattr(staff, attr, value)

    def get_attributes(self, staff):
        return {attr: getattr(staff, attr) for attr in self.STAFF_ATTRIBUTES}