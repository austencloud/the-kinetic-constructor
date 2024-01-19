# svg_manager.py

from typing import TYPE_CHECKING, Union
from PyQt6.QtSvg import QSvgRenderer
import re

from constants import BLUE, HEX_BLUE, HEX_RED, PROP_DIR, RED
from utilities.TypeChecking.MotionAttributes import MotionTypes, Turns
from utilities.TypeChecking.prop_types import PropTypes

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from objects.graphical_object.graphical_object import GraphicalObject


class SvgManager:
    def __init__(self, object: "GraphicalObject") -> None:
        self.object: Union["Arrow", "Prop"] = object
        self.renderer = None

    def set_svg_color(self, new_color: str) -> bytes:
        def replace_class_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        def replace_fill_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)
        with open(self.object.svg_file, "r") as f:
            svg_data = f.read()
        class_color_pattern = re.compile(
            r"(\.st0\s*\{\s*fill:\s*)(#[a-fA-F0-9]{6})(\s*;\s*\})"
        )
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)
        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.object.renderer: QSvgRenderer = QSvgRenderer(svg_file)
        self.object.setSharedRenderer(self.object.renderer)

    def update_svg(self, svg_file: str) -> None:
        self.set_svg_color(self.object.color)
        self.setup_svg_renderer(svg_file)

    def update_color(self) -> None:
        new_svg_data = self.set_svg_color(self.object.color)
        self.object.renderer.load(new_svg_data)
        if not self.object.is_ghost:
            self.object.ghost.renderer.load(new_svg_data)
        self.object.setSharedRenderer(self.object.renderer)

    def update_arrow_svg(self) -> None:
        svg_file = self.get_arrow_svg_file(self.object.motion_type, self.object.turns)
        self.object.svg_file = svg_file
        self.update_svg(svg_file)
        if not self.object.is_ghost and self.object.ghost:
            self.object.ghost.svg_manager.update_svg(svg_file)

    def get_arrow_svg_file(self, motion_type: MotionTypes, turns: Turns) -> str:
        cache_key = f"{motion_type}_{float(turns)}"
        if cache_key not in self.object.svg_cache:
            file_path = (
                f"resources/images/arrows/{self.object.pictograph.main_widget.grid_mode}/"
                f"{motion_type}/{motion_type}_{float(turns)}.svg"
            )
            with open(file_path, "r") as file:
                self.object.svg_cache[cache_key] = file.name
        return self.object.svg_cache[cache_key]

    def update_prop_svg(self) -> None:
        self.svg_file = self.get_prop_svg_file(self.object.prop_type)
        self.update_svg(self.svg_file)

    def get_prop_svg_file(self, prop_type: PropTypes) -> str:
        svg_file = f"{PROP_DIR}{prop_type}.svg"
        return svg_file