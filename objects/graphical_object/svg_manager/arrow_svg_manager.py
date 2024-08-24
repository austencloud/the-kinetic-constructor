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

    def update_arrow_svg(self, arrow: "Arrow") -> None:
        svg_file = self._get_arrow_svg_file(arrow)
        svg_data = self.manager.file_manager.load_svg_file(svg_file)
        colored_svg_data = self.manager.color_manager.apply_color_transformations(
            svg_data, arrow.color
        )
        self._setup_arrow_svg_renderer(arrow, colored_svg_data)

    def _get_arrow_svg_file(self, object: "Arrow") -> str:
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

    def _setup_arrow_svg_renderer(self, arrow: "Arrow", svg_data: str) -> None:
        arrow.renderer = QSvgRenderer()
        arrow.renderer.load(svg_data.encode("utf-8"))
        arrow.setSharedRenderer(arrow.renderer)
