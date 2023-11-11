from PyQt6.QtWidgets import QGraphicsItem
from objects.arrow import Arrow


class GhostArrow(Arrow):
    def __init__(self, graphboard, color):
        super().__init__(graphboard, None)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(self.center)
        self.graphboard = graphboard
        self.color = color
        self.target_arrow = None

    def update(self, target_arrow, drag=None):
        self.setOpacity(0.2)
        if drag:
            self.set_attributes_from_dict(drag.get_attributes())
        else:
            self.set_attributes_from_dict(target_arrow.get_attributes())

        self.update_svg(target_arrow.svg_file)
        self._setup_graphics_flags()
        self.update_appearance()
        self.show()
