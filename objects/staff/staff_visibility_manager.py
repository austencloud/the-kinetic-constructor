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
                staff.scene.removeItem(staff.arrow)

                staff.scene.arrow_manager.infobox.update()
                staff.scene.update_letter(
                    staff.scene.info_handler.determine_current_letter_and_type()[0]
                )
