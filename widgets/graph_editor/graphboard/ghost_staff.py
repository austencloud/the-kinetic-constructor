from objects.staff import Staff


class GhostStaff(Staff):
    def __init__(self, graphboard, color):
        super().__init__(graphboard, None)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(self.center)
        self.graphboard = graphboard
        self.color = color
        self.target_staff = None

    def update(self, new_quadrant, target_staff, drag=None):
        self.setOpacity(0.2)
        if drag:
            self.set_attributes_from_dict(drag.get_attributes())
        else:
            self.set_attributes_from_dict(target_staff.get_attributes())

        self.update_svg(target_staff.svg_file)
        self._setup_graphics_flags()
        self.update_appearance()
        self.quadrant = new_quadrant
        self.show()
