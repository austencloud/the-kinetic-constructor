from objects.arrow.arrow import Arrow

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class ArrowSvgCache:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.arrow_cache = {}

    def generate_key(self, attributes):
        return "_".join(map(str, attributes))

    def get_svg(self, attributes):
        key = self.generate_key(attributes)
        if key not in self.arrow_cache:
            self.arrow_cache[key] = self.load_svg_from_file(attributes)
        return self.arrow_cache[key]

    def load_svg_from_file(self, attributes):
        # Load the SVG file based on the attributes
        pass

    def update_svg(self, arrow: Arrow):
        attributes = self.extract_relevant_attributes(arrow)
        svg_data = self.get_svg(attributes)
        self.main_widget.svg_manager.update_svg(arrow)

    def extract_relevant_attributes(self, arrow: Arrow):
        return (arrow.motion.motion_type, arrow.motion.turns)
