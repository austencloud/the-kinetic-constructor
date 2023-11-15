from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from settings.string_constants import COLOR_MAP, CLOCKWISE, RED_HEX
import re
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard
    from objects.arrow import Arrow
    from objects.staff import Staff
    from objects.ghosts.ghost_staff import GhostStaff
    from objects.ghosts.ghost_arrow import GhostArrow
    
from utilities.TypeChecking.TypeChecking import (
    Color,
    ArrowAttributesDicts,
    StaffAttributesDicts,
)


class GraphicalObject(QGraphicsSvgItem):
    def __init__(self, svg_file: str, graphboard: "GraphBoard") -> None:
        super().__init__()
        self.svg_file = svg_file
        self.graphboard = graphboard
        
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

    def update(self, attributes) -> None:
        self.set_attributes_from_dict(attributes)
        self.update_appearance()

    def update_appearance(self: Union["Staff", "Arrow", "GhostStaff", "GhostArrow"]) -> None:
        from objects.staff import Staff 
        self.update_color()
        if isinstance(self, Staff):
            self.update_axis() 
        self.update_rotation()

    def set_attributes_from_dict(self, attributes: ArrowAttributesDicts | StaffAttributesDicts) -> None:
        self.attributes = self.apply_attributes(attributes)

    def apply_attributes(self, attributes: ArrowAttributesDicts | StaffAttributesDicts) -> dict:
        for attribute in attributes.keys():
            setattr(self, attribute, attributes[attribute])
        return {attribute: getattr(self, attribute) for attribute in attributes.keys()}

