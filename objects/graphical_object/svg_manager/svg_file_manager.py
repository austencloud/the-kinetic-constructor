from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )


class SvgFileManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

