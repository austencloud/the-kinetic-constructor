# svg_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
import re

from constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from objects.graphical_object.graphical_object import GraphicalObject


class GraphicalObjectSvgManager:
    def __init__(self, graphical_object: "GraphicalObject"):
        self.graphical_object = graphical_object
        self.renderer = None

    def set_svg_color(self, new_color: str) -> bytes:
        def replace_class_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        def replace_fill_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)
        with open(self.graphical_object.svg_file, "r") as f:
            svg_data = f.read()
        class_color_pattern = re.compile(
            r"(\.st0\s*\{\s*fill:\s*)(#[a-fA-F0-9]{6})(\s*;\s*\})"
        )
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)
        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.graphical_object.renderer: QSvgRenderer = QSvgRenderer(svg_file)
        self.graphical_object.setSharedRenderer(self.graphical_object.renderer)

    def update_svg(self, svg_file: str) -> None:
        self.set_svg_color(self.graphical_object.color)
        self.setup_svg_renderer(svg_file)

    def update_color(self) -> None:
        new_svg_data = self.set_svg_color(self.graphical_object.color)
        self.graphical_object.renderer.load(new_svg_data)
        if not self.graphical_object.is_ghost:
            self.graphical_object.ghost.renderer.load(new_svg_data)
        self.graphical_object.setSharedRenderer(self.graphical_object.renderer)
