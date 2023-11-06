from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *

class ArrowSelector:
    def __init__(self, arrow):
        self.arrow = arrow



    ### HELPERS ###

    def initialize_ghost_arrow(self, arrow, graphboard):
        deleted_arrow_attributes = arrow.attributes.get_attributes(arrow)
        ghost_attributes_dict = {
            COLOR: deleted_arrow_attributes[COLOR],
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            QUADRANT: "None",
            START_LOCATION: deleted_arrow_attributes[END_LOCATION],
            END_LOCATION: deleted_arrow_attributes[END_LOCATION],
            TURNS: 0,
        }

        ghost_arrow = self.arrow_manager.factory.create_arrow(
            graphboard, ghost_attributes_dict
        )

        graphboard.addItem(ghost_arrow)
        ghost_arrow.is_ghost = True
        ghost_arrow.setScale(GRAPHBOARD_SCALE)
        ghost_arrow.staff = arrow.staff
        ghost_arrow.staff.arrow = ghost_arrow
