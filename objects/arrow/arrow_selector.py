from objects.arrow.arrow import Arrow
from constants import GRAPHBOARD_SCALE

class ArrowSelector:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager


    def delete_staff(self, staffs):
        if staffs:
            # if staffs is not a list, make it a list
            if not isinstance(staffs, list):
                staffs = [staffs]
            for staff in staffs:
                ghost_arrow = staff.arrow if staff.arrow.is_ghost else None
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
                deleted_arrow_attributes = arrow.attributes.get_attributes(arrow)
                
                ghost_attributes_dict = {
                                'color': deleted_arrow_attributes['color'],
                                'motion_type': 'static',
                                'rotation_direction': 'None',
                                'quadrant': 'None',
                                'start_location': deleted_arrow_attributes['end_location'],
                                'end_location': deleted_arrow_attributes['end_location'],
                                'turns': 0
                }
                
                ghost_arrow = self.arrow_manager.arrow_factory.create_arrow(self.arrow_manager.graphboard_view, ghost_attributes_dict)
                ghost_arrow.is_ghost = True
                ghost_arrow.setScale(GRAPHBOARD_SCALE)
                ghost_arrow.staff = arrow.staff  
                ghost_arrow.staff.arrow = ghost_arrow
                
                graphboard_scene = self.arrow_manager.graphboard_view.scene()
                graphboard_scene.addItem(ghost_arrow)
                graphboard_scene.removeItem(arrow)
                
                self.arrow_manager.info_frame.update()
        else:
            print("No items selected")

