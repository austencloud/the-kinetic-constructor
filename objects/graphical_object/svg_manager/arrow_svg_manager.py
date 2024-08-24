from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow.arrow import Arrow
from data.constants import CLOCK, COUNTER, IN, OUT

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )


class ArrowSvgManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager

    def get_arrow_svg_file(self, object: "Arrow") -> str:
        start_ori = object.motion.start_ori
        if start_ori in [IN, OUT]:
            return get_images_and_data_path(
                f"images/arrows/{object.motion.motion_type}/from_radial/"
                f"{object.motion.motion_type}_{float(object.motion.turns)}.svg"
            )
        elif start_ori in [CLOCK, COUNTER]:
            return get_images_and_data_path(
                f"images/arrows/{object.motion.motion_type}/from_nonradial/"
                f"{object.motion.motion_type}_{float(object.motion.turns)}.svg"
            )

    def update_arrow_svg(self, object: "Arrow") -> None:
        svg_file = self.get_arrow_svg_file(object)
        svg_data = self.manager.file_manager.load_svg_file(svg_file)
        colored_svg_data = self.manager.color_manager.apply_color_transformations(
            svg_data, object.color
        )
        self.setup_svg_renderer(object, colored_svg_data)

    def setup_svg_renderer(self, object: "Arrow", svg_data: str) -> None:
        object.renderer = QSvgRenderer()
        object.renderer.load(svg_data.encode("utf-8"))
        object.setSharedRenderer(object.renderer)
