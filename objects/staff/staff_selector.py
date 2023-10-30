
class StaffSelector: 
    def __init__(self, staff_handler):
        self.staff_handler = staff_handler
        self.arrow_manager = staff_handler.main_widget.arrow_manager
       
    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                if staff.arrow:
                    ghost_arrow = staff.arrow if staff.arrow.is_ghost else None
                    if ghost_arrow:
                        self.arrow_manager.graphboard_view.scene().removeItem(ghost_arrow)
                        print(f"Ghost arrow for {staff.color} staff deleted")

                
                self.arrow_manager.graphboard_view.scene().removeItem(staff)
                self.arrow_manager.graphboard_view.scene().removeItem(staff.arrow)
                
                print(f"{staff.color} staff deleted")

                self.arrow_manager.info_frame.update()
                self.arrow_manager.graphboard_view.update_letter(self.arrow_manager.graphboard_view.info_handler.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")