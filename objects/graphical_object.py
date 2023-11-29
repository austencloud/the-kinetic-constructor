from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from settings.string_constants import COLOR_MAP
import re
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from objects.arrow import Arrow
    from objects.prop import Prop

from utilities.TypeChecking.TypeChecking import (
    Color,
    PropAttributesDicts,
    MotionAttributesDicts,
)


class GraphicalObject(QGraphicsSvgItem):
    self: Union["Prop", "Arrow"]    

    def __init__(self, svg_file: str, pictograph: "Pictograph") -> None:
        super().__init__()
        self.svg_file = svg_file
        self.pictograph = pictograph

        self.renderer: QSvgRenderer = None
        self.color: Color = None

        self.center = self.boundingRect().center()
        if svg_file:
            self.setup_svg_renderer(svg_file)
        self.setup_graphics_flags()

    def setup_graphics_flags(self) -> None:
        # Common flags setup for Arrow and Staff
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def set_svg_color(self, new_color: Color) -> bytes:
        new_hex_color = COLOR_MAP.get(new_color)

        with open(self.svg_file, "r") as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)

        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file: str) -> None:
        self.renderer: QSvgRenderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    def update_color(self) -> None:
        new_svg_data = self.set_svg_color(self.color)
        self.renderer.load(new_svg_data)
        self.setSharedRenderer(self.renderer)

    def update_svg(self, svg_file) -> None:
        self.svg_file = svg_file
        self.setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def update_attributes(self, attributes) -> None:
        self.set_attributes_from_dict(attributes)
        self.update_appearance()

    def update_appearance(self: Union["Prop", "Arrow"]) -> None:
        self.update_color()
        self.update_rotation()

    def set_attributes_from_dict(
        self, attributes: MotionAttributesDicts | PropAttributesDicts
    ) -> None:
        for attribute_name, attribute_value in attributes.items():
            setattr(self, attribute_name, attribute_value)

    def is_dim(self, on: bool) -> None:
        if on:
            self.setOpacity(0.25)  # Change opacity or use another effect to highlight
        else:
            self.setOpacity(1.0)  # Reset to normal when not highlighted
    

        
    def get_object_center(self) -> QPointF:
        if self.rotation() in [90, 270]:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
        elif self.rotation() in [0, 180]:
            return QPointF(
                (self.boundingRect().width() / 2), (self.boundingRect().height() / 2)
            )

    def mouseMoveEvent(self: Union["Prop", "Arrow"], event) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.get_object_center()
            self.set_drag_pos(new_pos)
            self.update_location(event.scenePos())