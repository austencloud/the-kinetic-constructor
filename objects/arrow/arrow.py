from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from events.drag.drag_manager import DragManager
from objects.arrow.arrow_attributes import ArrowAttributes
import re
from settings.string_constants import *


class Arrow(QGraphicsSvgItem):
    def __init__(self, scene, attr_dict):
        self.svg_file = self.get_svg_file(attr_dict)
        super().__init__(self.svg_file)
        self.initialize_svg_renderer(self.svg_file)
        self.initialize_app_attributes(scene, attr_dict)
        self.initialize_graphics_flags()

    def select(self):
        self.setSelected(True)

    def get_svg_file(self, attr_dict):
        motion_type = attr_dict[MOTION_TYPE]
        turns = attr_dict.get(TURNS, None)

        if motion_type in [PRO, ANTI]:
            self.is_shift = True
            return f"resources/images/arrows/shift/{motion_type}_{turns}.svg"
        elif motion_type in [STATIC]:
            self.is_static = True
            return None

    def initialize_app_attributes(self, scene, dict):
        if scene is not None:
            self.scene = scene
            if hasattr(scene, "infobox"):
                self.infobox = scene.infobox
            self.main_widget = scene.main_widget
            self.arrow_manager = self.main_widget.arrow_manager
            self.arrow_manager.arrow = self
            self.in_graphboard = False
            self.drag_offset = QPointF(0, 0)
            self.is_ghost = False
            self.staff = None
            self.is_mirrored = False
            self.previous_arrow = None
            self.drag_manager = self.main_widget.drag_manager

        self.attributes = self.main_widget.arrow_manager.attributes
        self.attributes.update_attributes(self, dict)
        self.update_appearance()
        self.center = self.boundingRect().center()

    def initialize_graphics_flags(self):
        flags = [
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable,
        ]

        for flag in flags:
            self.setFlag(flag, True)

        self.setTransformOriginPoint(self.center)

    def initialize_svg_renderer(self, svg_file):
        if getattr(self, "is_shift", False):
            self.renderer = QSvgRenderer(svg_file)
            self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.drag_start_pos = self.pos()
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        self.setSelected(True)
        if event.buttons() == Qt.MouseButton.LeftButton:
            from widgets.graph_editor.graphboard.graphboard import Graphboard
            from objects.pictograph.pictograph_view import PictographView

            if isinstance(self.scene, Graphboard):
                self.handle_graphboard_drag(event)
            elif isinstance(self.scene, PictographView):
                self.handle_pictograph_view_drag(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "future_position"):
            self.setPos(self.future_position)
            del self.future_position
        from widgets.graph_editor.graphboard.graphboard import Graphboard

        if isinstance(self.scene, Graphboard):
            self.arrow_manager.positioner.update_arrow_position(self.scene)

    def handle_graphboard_drag(self, event):
        """Dragging an arrow that is already in the graphboard"""
        new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
        self.setPos(new_pos)
        new_quadrant = self.scene.get_graphboard_quadrants(new_pos + self.center)
        if self.quadrant != new_quadrant:
            self.quadrant = new_quadrant
            self.update_appearance()
            (
                self.start_location,
                self.end_location,
            ) = self.attributes.get_start_end_locations(
                self.motion_type, self.rotation_direction, self.quadrant
            )
            self.staff.location = self.end_location
            self.staff.attributes.update_attributes_from_arrow(self)
            self.staff.handler.update_graphboard_staffs(self.scene.graphboard)
            self.scene.graphboard.update()
            self.scene.info_handler.update()

    def handle_pictograph_view_drag(self, event):
        new_pos = self.mapToScene(event.pos()) - self.drag_offset / 2
        self.setPos(new_pos)

    # UPDATE APPEARANCE

    def update_appearance(self):
        self.update_color()
        self.update_rotation()

    def set_svg_color(self, svg_file, new_color):
        color_map = {RED: RED_HEX, BLUE: BLUE_HEX}
        new_hex_color = color_map.get(new_color)

        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode("utf-8")

    def get_svg_data(self, svg_file):
        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def update_color(self):
        if self.motion_type in [PRO, ANTI]:
            new_svg_data = self.set_svg_color(self.svg_file, self.color)

            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)

    def update_rotation(self):
        angle = self.get_rotation_angle(
            self.quadrant, self.motion_type, self.rotation_direction
        )
        self.setRotation(angle)

    def get_rotation_angle(self, quadrant, motion_type, rotation_direction):
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            motion_type, rotation_direction
        )
        return quadrant_to_angle.get(quadrant, 0)

    def get_quadrant_to_angle_map(self, motion_type, rotation_direction):
        if motion_type == PRO:
            return {
                CLOCKWISE: {"ne": 0, "se": 90, "sw": 180, "nw": 270},
                COUNTER_CLOCKWISE: {"ne": 270, "se": 180, "sw": 90, "nw": 0},
            }.get(rotation_direction, {})
        elif motion_type == ANTI:
            return {
                CLOCKWISE: {"ne": 270, "se": 180, "sw": 90, "nw": 0},
                COUNTER_CLOCKWISE: {"ne": 0, "se": 90, "sw": 180, "nw": 270},
            }.get(rotation_direction, {})
        elif motion_type == STATIC:
            return {
                CLOCKWISE: {"ne": 0, "se": 0, "sw": 0, "nw": 0},
                COUNTER_CLOCKWISE: {"ne": 0, "se": 0, "sw": 0, "nw": 0},
            }.get(rotation_direction, {})

    def mirror_self(self):
        self.is_mirrored = not self.is_mirrored
        self.setScale(-self.scale())
