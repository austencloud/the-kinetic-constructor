from typing import TYPE_CHECKING, Union
from PyQt6.QtSvg import QSvgRenderer

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )


class SvgCacheManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager
        self.file_path_cache = {}
        self.svg_content_cache = {}

    def store_svg_data_in_cache(self, file_path: str, svg_data: str):
        self.svg_content_cache[file_path] = svg_data
