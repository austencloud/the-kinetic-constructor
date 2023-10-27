from objects.staff.staff import Staff

class StaffFactory:
    def __init__(self, staff_manager):
        self.staff_manager = staff_manager

    def create_staff(self, scene, staff_dict):
        staff = Staff(scene, staff_dict)
        return staff

''' 
staff_dict = {
            "color": "red",
            "location": "e",
            "layer": 1,
        }
        
'''

