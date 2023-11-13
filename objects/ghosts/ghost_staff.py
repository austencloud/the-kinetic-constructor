from objects.staff import Staff


class GhostStaff(Staff):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(self.center)
        self.graphboard = graphboard
        self.target_staff = None

