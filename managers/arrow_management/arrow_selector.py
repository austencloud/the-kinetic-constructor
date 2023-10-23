from objects.arrow import Arrow
from constants import GRAPHBOARD_SCALE

class ArrowSelector:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def select_all_arrows(self):
        for item in self.arrow_manager.graphboard_view.items():
            if isinstance(item, Arrow):
                item.setSelected(True)

    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                ghost_arrow = staff.arrow
                if ghost_arrow:
                    self.arrow_manager.graphboard_view.scene().removeItem(ghost_arrow)
                    print(f"Ghost arrow for {staff.color} staff deleted")

                staff.hide()
                self.arrow_manager.graphboard_view.scene().removeItem(staff)
                print(f"{staff.color} staff deleted")

                self.arrow_manager.info_frame.update()
                self.arrow_manager.graphboard_view.update_letter(self.arrow_manager.graphboard_view.info_manager.determine_current_letter_and_type()[0])
        else:
            print("No staffs selected")

    def delete_arrow(self, deleted_arrows):
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                ghost_arrow = Arrow(None, arrow.view, arrow.info_frame, arrow.svg_manager, self.arrow_manager, 'static', arrow.staff_manager, arrow.color, None, None, 0, None)
                ghost_arrow.is_ghost = True
                ghost_arrow.set_static_attributes_from_deleted_arrow(arrow)
                ghost_arrow.setScale(GRAPHBOARD_SCALE)
                self.arrow_manager.graphboard_scene.addItem(ghost_arrow)
                self.arrow_manager.graphboard_scene.removeItem(arrow)
                self.arrow_manager.info_frame.update()
        else:
            print("No items selected")

