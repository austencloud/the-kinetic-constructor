from utilities.path_helpers import get_images_and_data_path
from .arrow_svg_manager import ArrowSvgManager
from .prop_svg_manager import PropSvgManager
from .svg_file_manager import SvgFileManager
from .svg_color_manager import SvgColorManager


class SvgManager:
    def __init__(self) -> None:
        self.color_manager = SvgColorManager(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)

    def load_svg_file(self, svg_path: str) -> str:
        with open(get_images_and_data_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data
