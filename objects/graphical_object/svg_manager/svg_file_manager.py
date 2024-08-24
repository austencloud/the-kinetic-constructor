from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import GraphicalObjectSvgManager


class SvgFileManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager

    def get_or_load_svg_file(self, svg_path: str) -> str:
        if svg_path in self.manager.cache_manager.svg_content_cache:
            return self.manager.cache_manager.svg_content_cache[svg_path]

        with open(get_images_and_data_path(svg_path), "r") as file:
            svg_data = file.read()
            self.manager.cache_manager.store_svg_data_in_cache(svg_path, svg_data)
        return svg_data
