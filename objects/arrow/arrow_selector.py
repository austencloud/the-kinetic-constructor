from objects.arrow.arrow import Arrow
from resources.constants.constants import GRAPHBOARD_SCALE


class ArrowSelector:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    ### DELETERS ###

    def delete_arrow(self, deleted_arrows, keep_staff=False):
        view = self.arrow_manager.graphboard_view
        scene = view.scene()
        if not isinstance(deleted_arrows, list):
            deleted_arrows = [deleted_arrows]
        for arrow in deleted_arrows:
            if isinstance(arrow, Arrow):
                scene.removeItem(arrow)
                if keep_staff:
                    self.initialize_ghost_arrow(arrow, scene)
            view.info_handler.update()
        else:
            print("No items selected")

    ### HELPERS ###

    def initialize_ghost_arrow(self, arrow, scene):
        view = self.arrow_manager.graphboard_view
        deleted_arrow_attributes = arrow.attributes.get_attributes(arrow)
        ghost_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROT_DIR: "None",
            QUADRANT: "None",
            START: deleted_arrow_attributes[END],
            END: deleted_arrow_attributes[END],
            TURNS: 0,
        }

        ghost_arrow = self.arrow_manager.factory.create_arrow(
            view, ghost_attributes_dict
        )

        scene.addItem(ghost_arrow)
        ghost_arrow.is_ghost = True
        ghost_arrow.setScale(GRAPHBOARD_SCALE)
        ghost_arrow.staff = arrow.staff
        ghost_arrow.staff.arrow = ghost_arrow
