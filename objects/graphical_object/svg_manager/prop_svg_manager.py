from typing import TYPE_CHECKING
from data.constants import BLUE, PROP_DIR, RED
from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from objects.prop.prop import Prop
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )
from widgets.path_helpers.path_helpers import get_images_and_data_path

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from objects.prop.prop import Prop
from Enums.PropTypes import PropType
from data.constants import BLUE, RED, PROP_DIR

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )


class PropSvgManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager

    def get_prop_svg_file(self, object: "Prop") -> str:
        prop_type_str = object.prop_type.name.lower()
        if object.prop_type == PropType.Hand:
            return self._hand_svg_file(object)

        return f"{PROP_DIR}{prop_type_str}.svg"

    def _hand_svg_file(self, object: "Prop") -> str:
        if object.color == BLUE:
            return get_images_and_data_path("images/hands/left_hand.svg")
        elif object.color == RED:
            return get_images_and_data_path("images/hands/right_hand.svg")
        else:
            raise ValueError(f"Unrecognized hand color: {object.color}")

    def update_prop_svg(self, object: "Prop") -> None:
        svg_file = self.get_prop_svg_file(object)
        svg_data = self.manager.file_manager.load_svg_file(svg_file)
        if object.prop_type != PropType.Hand:
            colored_svg_data = self.manager.color_manager.apply_color_transformations(
                svg_data, object.color
            )
        else:
            colored_svg_data = svg_data
        self.setup_svg_renderer(object, colored_svg_data)

    def setup_svg_renderer(self, object: "Prop", svg_data: str) -> None:
        object.renderer = QSvgRenderer()
        object.renderer.load(svg_data.encode("utf-8"))
        object.setSharedRenderer(object.renderer)
