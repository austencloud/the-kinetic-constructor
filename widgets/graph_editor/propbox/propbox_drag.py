from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF, QSize
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from objects.props import Prop
from objects.arrow import Arrow, StaticArrow
from utilities.TypeChecking.TypeChecking import *
from typing import TYPE_CHECKING
from settings.string_constants import (
    IN,
    OUT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    COLOR,
    MOTION_TYPE,
    STATIC,
    ROTATION_DIRECTION,
    ARROW_LOCATION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
)


if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.propbox.propbox import PropBox


class PropBoxDrag(QWidget):
    def __init__(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        super().__init__(main_window)
        self.setParent(main_window)
        self._setup_dependencies(main_window, pictograph, propbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.attributes: PropAttributesDicts = {}

    def _setup_dependencies(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        self.propbox = propbox
        self.pictograph = pictograph
        self.main_window = main_window
        self.has_entered_pictograph_once = False
        self.current_rotation_angle = 0
        self.previous_location = None
        self.preview = None
        self.svg_file = None
        self.static_arrow = None

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.set_attributes(target_prop)
        pixmap = self.create_pixmap()
        self.preview.setPixmap(pixmap)
        self.prop_center = (
            self.target_prop.boundingRect().center() * self.pictograph.view.view_scale
        )
        self.current_rotation_angle = self.get_rotation_angle()

    def get_rotation_angle(self) -> RotationAngle:
        angle_map: Dict[Tuple[Layer, Orientation], Dict[Location, RotationAngle]] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }
        key = (self.layer, self.orientation)
        return angle_map.get(key, {}).get(self.prop_location, 0)

    def set_attributes(self, target_prop: "Prop") -> None:
        self.prop_type: PropType = target_prop.prop_type
        self.color: Color = target_prop.color
        self.prop_location: Location = target_prop.prop_location
        self.layer: Layer = target_prop.layer
        self.orientation: Orientation = target_prop.orientation
        self.ghost_prop = self.pictograph.ghost_props[self.color]
        self.ghost_prop.target_prop = target_prop

    def create_pixmap(self) -> None:
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        original_pixmap = QPixmap(scaled_size)
        self.setFixedSize(scaled_size)
        self.preview.setFixedSize(scaled_size)
        original_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(original_pixmap)
        renderer.render(painter)
        painter.end()

        angle = self.get_rotation_angle()
        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = original_pixmap.transformed(rotate_transform)
        self.setFixedSize(rotated_pixmap.size())
        self.preview.setFixedSize(rotated_pixmap.size())
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return rotated_pixmap

    ### UPDATERS ###

    def update_preview_for_new_location(self, new_location: Location) -> None:
        self.ghost_prop.prop_type = self.prop_type
        self.ghost_prop.color = self.color
        self.ghost_prop.prop_location = new_location
        self.ghost_prop.orientation = self.orientation
        self.ghost_prop.layer = self.layer

        self.prop_location = new_location
        self.ghost_prop.prop_location = new_location

        ghost_svg = self.ghost_prop.get_svg_file(self.prop_type)
        self.ghost_prop.update_svg(ghost_svg)
        self.ghost_prop.update_color()
        self.ghost_prop.update_axis(new_location)
        self.ghost_prop.update_rotation()

        if not self.static_arrow:
            self.create_static_arrow()
        self.update_static_arrow()

        self.current_rotation_angle = self.get_rotation_angle()
        rotated_pixmap = self.create_pixmap_with_rotation(self.current_rotation_angle)

        if self.current_rotation_angle in [90, 270]:
            new_size = QSize(rotated_pixmap.width(), rotated_pixmap.height())
        else:
            new_size = rotated_pixmap.size()

        self.setFixedSize(new_size)
        self.preview.setFixedSize(new_size)
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.ghost_prop not in self.pictograph.props:
            self.pictograph.props.append(self.ghost_prop)
        if self.ghost_prop not in self.pictograph.items():
            self.pictograph.addItem(self.ghost_prop)

        # remove the old motion from the pcitograph before adding the new one
        for motion in self.pictograph.motions[:]:
            if motion.color == self.color:
                self.pictograph.motions.remove(motion)



        self.pictograph.add_motion(self.ghost_prop.arrow, self.ghost_prop, IN, 1)

        self.ghost_prop.motion.arrow_location = self.prop_location
        self.ghost_prop.motion.start_location = self.prop_location
        self.ghost_prop.motion.end_location = self.prop_location

        self.ghost_prop.arrow = self.static_arrow
        self.ghost_prop.arrow.arrow_location = self.prop_location
        self.ghost_prop.arrow.start_location = self.prop_location
        self.ghost_prop.arrow.end_location = self.prop_location

        self.pictograph.update_pictograph()
        self.move_to_cursor(self.propbox.view.mapFromGlobal(self.pos()))

    def create_static_arrow(self) -> None:

        static_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: "None",
            ARROW_LOCATION: self.prop_location,
            START_LOCATION: self.prop_location,
            END_LOCATION: self.prop_location,
            TURNS: 0,
        }

        self.static_arrow = StaticArrow(self, static_arrow_dict)
        for arrow in self.pictograph.arrows[:]:
            if arrow.color == self.color:
                self.pictograph.removeItem(arrow)
                self.pictograph.arrows.remove(arrow)
        self.pictograph.addItem(self.static_arrow)
        self.pictograph.arrows.append(self.static_arrow)
        self.static_arrow.prop = self.ghost_prop
        self.static_arrow.prop.arrow = self.static_arrow

        if self.static_arrow not in self.pictograph.items():
            self.pictograph.addItem(self.static_arrow)

    def update_static_arrow(self) -> None:
        self.static_arrow.color = self.color
        self.static_arrow.arrow_location = self.prop_location
        self.static_arrow.start_location = self.prop_location
        self.static_arrow.end_location = self.prop_location
        self.static_arrow.prop = self.ghost_prop
        self.static_arrow.prop.arrow = self.static_arrow
        self.static_arrow.update_appearance()
        self.pictograph.update_pictograph()

    ### EVENT HANDLERS ###
    def handle_mouse_press(self, event_pos: QPoint) -> None:
        self.create_static_arrow()

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                if not self.has_entered_pictograph_once:
                    self.has_entered_pictograph_once = True
                    self.remove_same_color_objects()
                    self.pictograph.add_motion(
                        self.ghost_prop.arrow, self.ghost_prop, IN, 1
                    )

                pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
                view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(
                    pos_in_main_window
                )
                scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
                new_location = self.pictograph.get_nearest_handpoint(scene_pos)

                if self.previous_location != new_location and new_location:
                    self.previous_location = new_location
                    self.ghost_prop.arrow.arrow_location = new_location
                    self.ghost_prop.arrow.start_location = new_location
                    self.ghost_prop.arrow.end_location = new_location
                    self.ghost_prop.motion.arrow_location = new_location
                    self.ghost_prop.motion.start_location = new_location
                    self.ghost_prop.motion.end_location = new_location
                    self.update_preview_for_new_location(new_location)
                    self.ghost_prop.update_attributes(self.attributes)
                    self.pictograph.update_pictograph()

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_prop_on_pictograph()
        self.deleteLater()
        self.pictograph.update_pictograph()
        self.propbox.propbox_drag = None
        self.ghost_prop.arrow = None
        self.reset_drag_state()
        self.previous_location = None

    ### HELPERS ###

    def reset_drag_state(self) -> None:
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

    def place_prop_on_pictograph(self) -> None:
        self.pictograph.update_pictograph()
        self.pictograph.clearSelection()
        self.placed_prop = Prop(self.pictograph, self.ghost_prop.get_attributes())

        self.placed_prop.arrow = self.ghost_prop.arrow
        self.placed_prop.arrow.arrow_location = self.prop_location
        self.placed_prop.arrow.start_location = self.prop_location
        self.placed_prop.arrow.end_location = self.prop_location

        self.pictograph.add_motion(self.placed_prop.arrow, self.placed_prop, IN, 1)
        self.placed_prop.motion.arrow_location = self.prop_location
        self.placed_prop.motion.start_location = self.prop_location
        self.placed_prop.motion.end_location = self.prop_location

        self.ghost_prop.arrow.prop = self.placed_prop
        self.pictograph.addItem(self.placed_prop)
        self.pictograph.props.append(self.placed_prop)

        self.pictograph.removeItem(self.ghost_prop)
        self.pictograph.props.remove(self.ghost_prop)

        self.placed_prop.ghost_prop = self.ghost_prop
        self.placed_prop.update_appearance()
        self.placed_prop.show()
        self.placed_prop.setSelected(True)

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    def remove_same_color_objects(self) -> None:
        for prop in self.pictograph.props[:]:
            if prop.isVisible() and prop.color == self.color:
                self.pictograph.removeItem(prop)
                self.pictograph.props.remove(prop)
        for arrow in self.pictograph.arrows[:]:
            if arrow.isVisible() and arrow.color == self.color:
                if isinstance(arrow, StaticArrow):
                    self.ghost_prop.arrow = arrow
                self.pictograph.removeItem(arrow)
                self.pictograph.arrows.remove(arrow)
        for motion in self.pictograph.motions[:]:
            if motion.color == self.color:
                self.pictograph.motions.remove(motion)

    def create_pixmap_with_rotation(self, angle: RotationAngle) -> QPixmap:
        # Generate a new pixmap based on target prop and apply the rotation
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)

        renderer.render(painter)
        painter.end()
        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(rotate_transform)

        return rotated_pixmap

    def start_drag(self, event_pos: "QPoint") -> None:
        self.move_to_cursor(event_pos)
        self.show()

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.propbox.view.mapTo(self.main_window, event_pos)
        self.center = QPointF((self.width() / 2), self.height() / 2)
        self.move(local_pos - self.center.toPoint())
