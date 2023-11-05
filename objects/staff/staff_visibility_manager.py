from objects.staff.staff import Staff


class StaffVisibilityManager:
    def __init__(self, staff_manager):
        self.staff_manager = staff_manager

    def hide_all_staffs(self, scene):
        for item in scene.items():
            if isinstance(item, Staff):
                item.setVisible(False)

    def hide_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                staff.hide()
                staff.view.scene().removeItem(staff.arrow)

                staff.view.arrow_manager.infobox.update()
                staff.view.update_letter(
                    staff.view.info_handler.determine_current_letter_and_type()[0]
                )
        else:
            print("No staffs selected")
