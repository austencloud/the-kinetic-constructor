from typing import TYPE_CHECKING, Union
from PyQt6.QtSvg import QSvgRenderer
import re

from constants import (
    ANTI,
    CLOCK,
    COUNTER,
    DASH,
    HEX_BLUE,
    HEX_RED,
    IN,
    NONRADIAL,
    OUT,
    PRO,
    PROP_DIR,
    RADIAL,
    STATIC,
)
from Enums.MotionAttributes import Color, MotionType, Turns
from Enums.PropTypes import PropType, PropTypeslist

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObjectSvgManager:
    svg_cache = {}

    def __init__(self) -> None:
        self.renderer = None

    @staticmethod
    def preload_svg_cache():
        turns = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        motion_types = [ANTI, PRO, DASH, STATIC]
        start_orientations = [RADIAL, NONRADIAL]
        for motion_type in motion_types:
            for turn in turns:
                for orientation in start_orientations:
                    GraphicalObjectSvgManager._preload_arrow_svg(
                        motion_type, turn, orientation
                    )

        prop_types = [p for p in PropTypeslist]
        for prop_type in prop_types:
            GraphicalObjectSvgManager._preload_prop_svg_path(prop_type)

    @staticmethod
    def _preload_arrow_svg(motion_type, turns, start_ori):
        cache_key = f"{motion_type}_{turns}_{start_ori}"
        file_path = (
            f"images/arrows/{motion_type}/from_{start_ori}/{motion_type}_{turns}.svg"
        )
        GraphicalObjectSvgManager.svg_cache[cache_key] = file_path

    @staticmethod
    def _preload_prop_svg_path(prop_type):
        cache_key = f"prop_{prop_type}"
        file_path = f"images/props/{prop_type}.svg"
        GraphicalObjectSvgManager.svg_cache[cache_key] = file_path

    def set_svg_color(self, new_color: str, object: Union["Arrow", "Prop"]) -> bytes:
        def replace_class_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        def replace_fill_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        COLOR_MAP = {Color.RED: HEX_RED, Color.BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)
        with open(object.svg_file, "r") as f:
            svg_data = f.read()
        class_color_pattern = re.compile(
            r"(\.st0\s*\{.*?fill:\s*)(#[a-fA-F0-9]{6})(.*?\})"
        )
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)
        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str, object: Union["Arrow", "Prop"]) -> None:
        object.renderer = QSvgRenderer(svg_file)
        object.setSharedRenderer(object.renderer)

    def update_color(self, object: Union["Arrow", "Prop"]) -> None:
        new_svg_data = self.set_svg_color(object.color, object)
        object.renderer.load(new_svg_data)
        object.setSharedRenderer(object.renderer)

    def update_svg(self, object: Union["Arrow", "Prop"]) -> None:
        svg_file = self.get_svg_file(object)
        if object.svg_file != svg_file or not object.renderer:
            object.svg_file = svg_file
            self.set_svg_color(object.color, object)
            self.setup_svg_renderer(svg_file, object)
        else:
            self.update_color(object)

    def _determine_svg_file(self, object: Union["Arrow", "Prop"]) -> str:
        """Determines the SVG file path based on object properties, without using cache."""
        if self.is_arrow(object):
            return self._arrow_svg_file(
                object.motion.motion_type, object.motion.turns, object
            )
        elif self.is_prop(object):
            return self._prop_svg_file(object.prop_type)

    def get_svg_file(self, object: Union["Arrow", "Prop"]) -> str:
        cache_key = self._generate_cache_key(object)
        if cache_key in GraphicalObjectSvgManager.svg_cache:
            return GraphicalObjectSvgManager.svg_cache[cache_key]

        svg_file = self._determine_svg_file(object)
        GraphicalObjectSvgManager.svg_cache[cache_key] = svg_file
        return svg_file

    def _generate_cache_key(self, object: Union["Arrow", "Prop"]) -> str:
        """Generates a unique key for caching based on object properties."""
        if self.is_arrow(object):
            if object.motion.start_ori in [IN, OUT]:
                return (
                    f"{object.motion.motion_type}_{float(object.motion.turns)}_radial"
                )
            elif object.motion.start_ori in [CLOCK, COUNTER]:
                return f"{object.motion.motion_type}_{float(object.motion.turns)}_nonradial"
        elif self.is_prop(object):
            return f"prop_{object.prop_type.name.lower()}"
        else:
            raise ValueError(
                f"Unsupported graphical object type: {object.__class__.__name__}"
            )

    def is_arrow(self, object: Union["Arrow", "Prop"]):
        return object.__class__.__name__ in ["Arrow"]

    def is_prop(self, object: Union["Arrow", "Prop"]):
        return "Prop" in [base.__name__ for base in object.__class__.__bases__]

    def _arrow_svg_file(
        self, motion_type: MotionType, turns: Turns, object: Union["Arrow", "Prop"]
    ) -> str:
        start_ori = object.motion.start_ori
        cache_key = f"{motion_type}_{float(turns)}_{start_ori}"  # Include start orientation in the cache key

        if cache_key not in object.svg_cache:
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
                object.svg_cache[cache_key] = file.name

        return object.svg_cache[cache_key]

    def _prop_svg_file(self, prop_type: PropType) -> str:
        prop_type_str = prop_type.name.lower()
        svg_file = f"{PROP_DIR}{prop_type_str}.svg"
        return svg_file


GraphicalObjectSvgManager.preload_svg_cache()
