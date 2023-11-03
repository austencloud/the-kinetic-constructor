from objects.arrow.arrow import Arrow
from resources.constants import GRAPHBOARD_SCALE


class ArrowSelector:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def delete_arrow(self, deleted_arrows):
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                deleted_arrow_attributes = arrow.attributes.get_attributes(arrow)

                ghost_attributes_dict = {
                    "color": deleted_arrow_attributes["color"],
                    "motion_type": "static",
                    "rotation_direction": "None",
                    "quadrant": "None",
                    "start_location": deleted_arrow_attributes["end_location"],
                    "end_location": deleted_arrow_attributes["end_location"],
                    "turns": 0,
                }

                ghost_arrow = self.arrow_manager.factory.create_arrow(
                    self.arrow_manager.graphboard_view, ghost_attributes_dict
                )
                ghost_arrow.is_ghost = True
                ghost_arrow.setScale(GRAPHBOARD_SCALE)
                ghost_arrow.staff = arrow.staff
                arrow.staff.arrow = ghost_arrow

                graphboard_scene = self.arrow_manager.graphboard_view.scene()
                graphboard_scene.addItem(ghost_arrow)
                graphboard_scene.removeItem(arrow)

                view = self.arrow_manager.graphboard_view
                view.info_handler.update()

        else:
            print("No items selected")
