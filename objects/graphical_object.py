from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
import re
from typing import TYPE_CHECKING, Union

from Enums import *
from constants.string_constants import RED, BLUE, HEX_RED, HEX_BLUE

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    self: Union["Prop", "Arrow"]

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

        self.renderer: QSvgRenderer = None
        self.color: Color = None

        self.center = self.boundingRect().center()

        self.setup_graphics_flags()

    ### SETUP ###

    def setup_graphics_flags(self) -> None:
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def set_svg_color(self, new_color: str) -> bytes:
        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)

        with open(self.svg_file, "r") as f:
            svg_data = f.read()

        # This regex pattern looks for the class color definition in the style tag
        class_color_pattern = re.compile(
            r"(\.st0\s*\{\s*fill:\s*)(#[a-fA-F0-9]{6})(\s*;\s*\})"
        )

        # This function will replace the old color with the new color
        def replace_class_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        # Replace all occurrences of the class color definition
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)

        # This regex pattern looks for the fill attribute and captures the color value
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')

        # This function will replace the old color with the new color
        def replace_fill_color(match: re.Match):
            return match.group(1) + new_hex_color + match.group(3)

        # Replace all occurrences of the fill color
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)

        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.renderer: QSvgRenderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    ### UPDATERS ###

    def update_color(self) -> None:
        new_svg_data = self.set_svg_color(self.color)
        self.renderer.load(new_svg_data)
        self.setSharedRenderer(self.renderer)

    def update_svg(self, svg_file) -> None:
        self.svg_file = svg_file
        self.setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_appearance(self: Union["Prop", "Arrow"]) -> None:
        self.update_color()
        self.update_rotation()

    def update_attributes(
        self, attributes: MotionAttributesDicts | PropAttributesDicts
    ) -> None:
        for attribute_name, attribute_value in attributes.items():
            setattr(self, attribute_name, attribute_value)

    ### FLAGS ###

    def is_dim(self, on: bool) -> None:
        if on:
            self.setOpacity(0.25)
        else:
            self.setOpacity(1.0)

    ### GETTERS ###

    def get_object_center(self) -> QPointF:
        if self.rotation() in [90, 270]:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
        elif self.rotation() in [0, 180]:
            return QPointF(
                (self.boundingRect().width() / 2), (self.boundingRect().height() / 2)
            )
