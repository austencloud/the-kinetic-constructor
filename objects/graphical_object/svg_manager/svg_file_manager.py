from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )


class SvgFileManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager

    def load_svg_file(self, svg_path: str) -> str:
        with open(get_images_and_data_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data
