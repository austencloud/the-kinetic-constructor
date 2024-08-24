from typing import TYPE_CHECKING
from widgets.path_helpers.path_helpers import get_images_and_data_path
from PyQt6.QtSvg import QSvgRenderer
from objects.arrow.arrow import Arrow
from data.constants import (
    CLOCK,
    COUNTER,
    IN,
    OUT,
    RADIAL,
    NONRADIAL,
    ANTI,
    PRO,
    DASH,
    STATIC,
)

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        GraphicalObjectSvgManager,
    )






class ArrowSvgManager:
    def __init__(self, manager: "GraphicalObjectSvgManager"):
        self.manager = manager

    def preload_svgs(self):
        motion_types = [ANTI, PRO, DASH, STATIC]
        turns = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        start_orientations = [RADIAL, NONRADIAL]

        for motion_type in motion_types:
            for turn in turns:
                for orientation in start_orientations:
                    cache_key = f"{motion_type}_{turn}_{orientation}"
                    file_path = get_images_and_data_path(
                        f"images/arrows/{motion_type}/from_{orientation}/{motion_type}_{turn}.svg"
                    )
                    self.manager.cache_manager.file_path_cache[cache_key] = file_path

    def get_arrow_svg_file(self, object: "Arrow") -> str:
        start_ori = object.motion.start_ori
        cache_key = (
            f"{object.motion.motion_type}_{float(object.motion.turns)}_{start_ori}"
        )

        if cache_key not in object.svg_cache:
            if start_ori in [IN, OUT]:
                file_path = (
                    f"images/arrows/{object.motion.motion_type}/from_radial/"
                    f"{object.motion.motion_type}_{float(object.motion.turns)}.svg"
                )
            elif start_ori in [CLOCK, COUNTER]:
                file_path = (
                    f"images/arrows/{object.motion.motion_type}/from_nonradial/"
                    f"{object.motion.motion_type}_{float(object.motion.turns)}.svg"
                )

            with open(file_path, "r") as file:
                object.svg_cache[cache_key] = file.name

        return object.svg_cache[cache_key]

    def update_arrow_svg(self, object: "Arrow") -> None:
        svg_file = self.get_arrow_svg_file(object)
        svg_data = self.manager.file_manager.get_or_load_svg_file(svg_file)
        colored_svg_data = self.manager.color_manager.apply_color_transformations(
            svg_data, object.color
        )
        self.setup_svg_renderer(object, colored_svg_data)

    def setup_svg_renderer(self, object: "Arrow", svg_data: str) -> None:
        object.renderer = QSvgRenderer()
        object.renderer.load(svg_data.encode("utf-8"))
        object.setSharedRenderer(object.renderer)
