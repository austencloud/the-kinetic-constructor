from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
import re
from typing import TYPE_CHECKING, Dict, Union


from constants import RED, BLUE, HEX_RED, HEX_BLUE
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow import Arrow
    from objects.prop.prop import Prop


class GraphicalObject(QGraphicsSvgItem):
    self: Union["Prop", "Arrow"]

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

        self.renderer: QSvgRenderer = None
        self.color: Colors = None

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
        def replace_class_color(match: re.Match) -> str:
            return match.group(1) + new_hex_color + match.group(3)

        def replace_fill_color(match: re.Match):
            return match.group(1) + new_hex_color + match.group(3)

        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)
        with open(self.svg_file, "r") as f:
            svg_data = f.read()
        class_color_pattern = re.compile(
            r"(\.st0\s*\{\s*fill:\s*)(#[a-fA-F0-9]{6})(\s*;\s*\})"
        )
        svg_data = class_color_pattern.sub(replace_class_color, svg_data)
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')
        svg_data = fill_pattern.sub(replace_fill_color, svg_data)
        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.renderer: QSvgRenderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    ### UPDATERS ###

    def _update_color(self: Union["Arrow", "Prop"]) -> None:
        new_svg_data = self.set_svg_color(self.color)
        self.renderer.load(new_svg_data)
        if not self.is_ghost:
            self.ghost.renderer.load(new_svg_data)
        self.setSharedRenderer(self.renderer)

    def update_svg(self, svg_file: str) -> None:
        self.set_svg_color(self.color)
        self.setup_svg_renderer(svg_file)

    def update_attributes(self, attributes: Dict) -> None:
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
