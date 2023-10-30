from objects.arrow.arrow import Arrow

class ArrowFactory:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def create_arrow(self, view, arrow_dict):
        arrow = Arrow(view, arrow_dict)
        return arrow

    def clone_arrow(self, arrow):
        arrow_dict = arrow.attributes.get_attributes(arrow)
        clone_arrow = self.create_arrow(self.arrow_manager.graphboard_view, arrow_dict)
        return clone_arrow