# svg_manager.py

from typing import TYPE_CHECKING, Union
from PyQt6.QtSvg import QSvgRenderer
import re

from constants import (
    ANTI,
    BLUE,
    CLOCK,
    COUNTER,
    HEX_BLUE,
    HEX_RED,
    IN,
    OUT,
    PRO,
    PROP_DIR,
    RED,
)
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
            r"(\.st0\s*\{.*?fill:\s*)(#[a-fA-F0-9]{6})(.*?\})"
        )
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)
        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.object.renderer = QSvgRenderer(svg_file)
        self.object.setSharedRenderer(self.object.renderer)

    def update_color(self) -> None:
        new_svg_data = self.set_svg_color(self.object.color)
        self.object.renderer.load(new_svg_data)
        self.object.setSharedRenderer(self.object.renderer)

    def update_svg(self) -> None:
        svg_file = self.get_svg_file()
        self.object.svg_file = svg_file
        self.set_svg_color(self.object.color)
        self.setup_svg_renderer(svg_file)

    def get_svg_file(self) -> str:
        if self.object.__class__.__name__ in ["Arrow", "GhostArrow"]:
            return self._arrow_svg_file(self.object.motion.motion_type, self.object.turns)
        elif "Prop" in [base.__name__ for base in self.object.__class__.__bases__]:
            return self._prop_svg_file(self.object.prop_type)
        else:
            raise ValueError(
                f"Unsupported graphical object type: {self.object.__class__.__name__}"
            )

    def _arrow_svg_file(self, motion_type: MotionTypes, turns: Turns) -> str:
        start_ori = self.object.motion.start_ori
        cache_key = f"{motion_type}_{float(turns)}_{start_ori}"  # Include start orientation in the cache key

        if cache_key not in self.object.svg_cache:
            if start_ori in [IN, OUT]:
                file_path = (
                    f"images/arrows/"
                    f"{motion_type}/from_radial/{motion_type}_{float(turns)}.svg"
                )
            elif start_ori in [CLOCK, COUNTER]:
                file_path = (
                    f"images/arrows/"
                    f"{motion_type}/from_nonradial/{motion_type}_{float(turns)}.svg"
                )

            with open(file_path, "r") as file:
                self.object.svg_cache[cache_key] = file.name

        return self.object.svg_cache[cache_key]

    def _prop_svg_file(self, prop_type: PropTypes) -> str:
        svg_file = f"{PROP_DIR}{prop_type}.svg"
        return svg_file
