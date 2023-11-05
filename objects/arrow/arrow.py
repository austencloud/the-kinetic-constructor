from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from events.drag.drag_manager import DragManager
from objects.arrow.arrow_attributes import ArrowAttributes
import re
from resources.constants import RED_HEX, BLUE_HEX, PRO, ANTI, STATIC, RED, BLUE


class Arrow(QGraphicsSvgItem):
    def __init__(self, view, attr_dict):
        self.svg_file = self.get_svg_file(attr_dict)
        super().__init__(self.svg_file)
        self.initialize_svg_renderer(self.svg_file)
        self.initialize_app_attributes(view, attr_dict)
        self.initialize_graphics_flags()

    def select(self):
        self.setSelected(True)

    def get_svg_file(self, attr_dict):
        motion_type = attr_dict["motion_type"]
        turns = attr_dict.get("turns", None)

        if motion_type in [PRO, ANTI]:
            self.is_shift = True
            return f"resources/images/arrows/shift/{motion_type}_{turns}.svg"
        elif motion_type in [STATIC]:
            self.is_static = True
            return None

    def initialize_app_attributes(self, view, dict):
        if view is not None:
            self.view = view
            if self.view.infobox is not None:
                self.infobox = view.infobox
            self.main_widget = view.main_widget
            self.arrow_manager = self.main_widget.arrow_manager
            self.arrow_manager.arrow = self
            self.in_graphboard = False
            self.drag_offset = QPointF(0, 0)
            self.is_ghost = False
            self.staff = None
            self.is_mirrored = False
            self.previous_arrow = None
            self.drag_manager = self.main_widget.drag_manager
            self.setScale(view.view_scale)

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
            from widgets.graph_editor.graphboard.graphboard_view import GraphboardView
            from objects.pictograph.pictograph_view import PictographView

            if isinstance(self.view, GraphboardView):
                self.handle_graphboard_view_drag(event)
            elif isinstance(self.view, PictographView):
                self.handle_pictograph_view_drag(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "future_position"):
            self.setPos(self.future_position)
            del self.future_position
        from widgets.graph_editor.graphboard.graphboard_view import GraphboardView

        if isinstance(self.view, GraphboardView):
            self.arrow_manager.positioner.update_arrow_position(self.view)

    def handle_graphboard_view_drag(self, event):
        """Dragging an arrow that is already in the graphboard"""
        new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
        self.setPos(new_pos)
        new_quadrant = self.view.get_graphboard_quadrants(new_pos + self.center)
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
            self.staff.handler.update_graphboard_staffs(self.view.graphboard_scene)
            self.view.graphboard_scene.update()
            self.view.info_handler.update()

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

        with open(svg_file, "r") as f:
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
        with open(svg_file, "r") as f:
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
                "r": {"ne": 0, "se": 90, "sw": 180, "nw": 270},
                "l": {"ne": 270, "se": 180, "sw": 90, "nw": 0},
            }.get(rotation_direction, {})
        elif motion_type == ANTI:
            return {
                "r": {"ne": 270, "se": 180, "sw": 90, "nw": 0},
                "l": {"ne": 0, "se": 90, "sw": 180, "nw": 270},
            }.get(rotation_direction, {})
        elif motion_type == STATIC:
            return {
                "r": {"ne": 0, "se": 0, "sw": 0, "nw": 0},
                "l": {"ne": 0, "se": 0, "sw": 0, "nw": 0},
            }.get(rotation_direction, {})

    def mirror_self(self):
        self.is_mirrored = not self.is_mirrored
        self.setScale(-self.scale())
