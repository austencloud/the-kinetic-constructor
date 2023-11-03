from objects.staff.staff import Staff

class StaffVisibilityManager:
    def __init__(self, staff_manager):
        self.staff_manager = staff_manager
    
    def hide_all_staffs(self, scene):
        for item in scene.items():
            if isinstance(item, Staff):
                item.setVisible(False)
       
    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                if staff.arrow:
                    ghost_arrow = staff.arrow if staff.arrow.is_ghost else None
                    if ghost_arrow:
                        ghost_arrow.hide()

                staff.hide()
                self.arrow_manager.graphboard_view.scene().removeItem(staff.arrow)
                
                self.arrow_manager.info_frame.update()
                self.arrow_manager.graphboard_view.update_letter(self.arrow_manager.graphboard_view.info_handler.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")