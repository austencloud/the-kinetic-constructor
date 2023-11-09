from PyQt6.QtWidgets import QGraphicsItem
from objects.arrow.arrow import GhostArrow


class GhostArrowManager:
    def __init__(self, graphboard):
        self.graphboard = graphboard

    def init_ghost_arrow(self):
        self.ghost_arrow = GhostArrow(self.graphboard, None)
        return self.ghost_arrow

    def update_ghost_arrow(self, new_quadrant, target_arrow):
        self.ghost_arrow.setOpacity(0.2)
        self.ghost_arrow.set_object_attr_from_dict(target_arrow.get_attributes())
        self.ghost_arrow.update_svg(self.ghost_arrow.target_arrow.svg_file)
        self.ghost_arrow.setup_graphics_flags()
        self.ghost_arrow.update_appearance()
        self.ghost_arrow.quadrant = new_quadrant
        self.ghost_arrow.show()  #

    def update_staff(self, graphboard, staff):
        staff.location = self.ghost_arrow.end_location
        staff.update_attributes_from_arrow(self.ghost_arrow)
        graphboard.update()
