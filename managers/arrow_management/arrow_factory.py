from objects.arrow import Arrow

class ArrowFactory:
    def __init__(self, arrow_manager):
        self.arrow_manager = arrow_manager

    def create_arrow(self, view, arrow_dict):
        svg_file = f"images/arrows/shift/{arrow_dict['motion_type']}_{arrow_dict['turns']}.svg"
        arrow = Arrow(svg_file, 
                        view,                         
                        arrow_dict)

        return arrow

