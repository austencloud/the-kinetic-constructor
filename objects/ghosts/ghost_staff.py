from objects.staff import Staff


class GhostStaff(Staff):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(self.center)
        self.graphboard = graphboard
        self.target_staff = None

    def update(self, target_staff, drag=None):
        if drag:
            self.set_attributes_from_dict(drag.get_attributes())
        else:
            self.set_attributes_from_dict(target_staff.get_attributes())

        self.setup_graphics_flags()
        self.update_appearance()
        self.show()
