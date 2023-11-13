from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from settings.string_constants import COLOR_MAP, CLOCKWISE
import re

class GraphicalObject(QGraphicsSvgItem):
    def __init__(self, svg_file, graphboard, attributes):
        super().__init__()
        self.svg_file = svg_file
        self.graphboard = graphboard
        self.attributes = attributes
        
        self.type = None
        self.center = self.boundingRect().center()
        if svg_file:
            self.setup_svg_renderer(svg_file)
        self.setup_graphics_flags()
        
    def setup_graphics_flags(self):
        # Common flags setup for Arrow and Staff
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def set_svg_color(self, new_color):
        new_hex_color = COLOR_MAP.get(new_color)

        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)

        return svg_data.encode("utf-8")

    def setup_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    def update_color(self):
        new_svg_data = self.set_svg_color(self.color)
        self.renderer.load(new_svg_data)
        self.setSharedRenderer(self.renderer)

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self.setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)
        
    def update(self, attributes):
        self.set_attributes_from_dict(attributes)
        self.update_appearance()