from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from settings.string_constants import (
    ANTI,
    ARROW_LOCATION,
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    END_LOCATION,
    IN,
    LAYER,
    LOCATION,
    MOTION_TYPE,
    NORTHEAST,
    NORTHWEST,
    PRO,
    PROP_LOCATION,
    RED,
    ROTATION_DIRECTION,
    SOUTHEAST,
    SOUTHWEST,
    START_LOCATION,
    TURNS,
)
from objects.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.arrowbox.arrowbox import ArrowBox
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    Color,
    MotionType,
    Location,
    RotationDirection,
    Location,
    Turns,
    RotationAngle,
)


class ArrowBoxDrag(QWidget):
    def __init__(
        self, main_window: "MainWindow", pictograph: "Pictograph", arrowbox: "ArrowBox"
    ) -> None:
        super().__init__()
        self.setParent(main_window)
        self._setup_dependencies(main_window, pictograph, arrowbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.attributes: ArrowAttributesDicts = {}
        self.reset_drag_state()

    def _setup_dependencies(
        self, main_window: "MainWindow", pictograph: "Pictograph", arrowbox: "ArrowBox"
    ) -> None:
        self.arrowbox = arrowbox
        self.pictograph = pictograph
        self.main_window = main_window
        self.has_entered_pictograph_once = False
        self.current_rotation_angle = 0
        self.previous_location = None
        self.preview = None
        self.svg_file = None
        self.ghost_arrow = None
        self.start_orientation = IN

    def match_target_arrow(self, target_arrow: "Arrow") -> None:
        self.target_arrow = target_arrow
        self.set_attributes(target_arrow)
        pixmap = self.create_pixmap(target_arrow)
        self.preview.setPixmap(pixmap)
        self.preview.setFixedHeight(pixmap.height())
        self.arrow_center = (
            self.target_arrow.boundingRect().center() * self.pictograph.view.view_scale
        )
        self.current_rotation_angle = target_arrow.get_rotation_angle()
        self.is_svg_mirrored = target_arrow.is_svg_mirrored
        self.preview.setPixmap(pixmap)
        self.apply_transformations_to_preview()

    def set_attributes(self, target_arrow: "Arrow") -> None:
        self.color: Color = target_arrow.color
        self.motion_type: MotionType = target_arrow.motion_type
        self.arrow_location: Location = target_arrow.arrow_location
        self.rotation_direction: RotationDirection = target_arrow.rotation_direction
        self.start_location: Location = target_arrow.start_location
        self.end_location: Location = target_arrow.end_location
        self.turns: Turns = target_arrow.turns

        self.ghost_arrow = self.pictograph.ghost_arrows[self.color]
        self.ghost_arrow.target_arrow = target_arrow

    def reset_drag_state(self) -> None:
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

    def create_pixmap(self, target_arrow: "Arrow") -> QPixmap:
        new_svg_data = target_arrow.set_svg_color(target_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)
        return pixmap

    def get_attributes(self) -> ArrowAttributesDicts:
        start_location: Location
        end_location: Location
        (
            start_location,
            end_location,
        ) = self.target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.arrow_location
        )

        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            ARROW_LOCATION: self.arrow_location,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: start_location,
            END_LOCATION: end_location,
            TURNS: self.turns,
        }

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.arrowbox.view.mapTo(self.main_window, event_pos)
        self.move(local_pos - (self.arrow_center).toPoint())

    def remove_same_color_arrow(self) -> None:
        for arrow in self.pictograph.arrows[:]:
            if arrow.isVisible() and arrow.color == self.color:
                self.pictograph.removeItem(arrow)
                self.pictograph.arrows.remove(arrow)
        for prop in self.pictograph.props[:]:
            if prop.isVisible() and prop.color == self.color:
                self.pictograph.removeItem(prop)
                self.pictograph.props.remove(prop)

    def place_arrow_on_pictograph(self) -> None:
        self.pictograph.update_pictograph()
        self.pictograph.clearSelection()
        self.placed_arrow = Arrow(self.pictograph, self.ghost_arrow.get_attributes())
        self.placed_arrow.prop = self.ghost_arrow.prop
        self.ghost_arrow.prop.arrow = self.placed_arrow

        self.pictograph.add_motion(
            self.placed_arrow,
            self.ghost_arrow.prop,
            IN,
            1,
        )

        self.pictograph.addItem(self.placed_arrow)
        self.pictograph.arrows.append(self.placed_arrow)

        self.pictograph.removeItem(self.ghost_arrow)
        self.pictograph.arrows.remove(self.ghost_arrow)

        self.placed_arrow.ghost_arrow = self.ghost_arrow
        self.placed_arrow.update_appearance()
        self.placed_arrow.show()
        self.placed_arrow.setSelected(True)

    def start_drag(self, event_pos: "QPoint") -> None:
        self.move_to_cursor(event_pos)
        self.show()

    ### EVENT HANDLERS ###

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                self.handle_enter_pictograph(event_pos)

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_arrow_on_pictograph()
        self.deleteLater()
        self.pictograph.update_pictograph()
        self.arrowbox.arrowbox_drag = None
        self.ghost_arrow.prop = None
        self.reset_drag_state()

    def handle_enter_pictograph(self, event_pos: QPoint) -> None:
        if not self.has_entered_pictograph_once:
            self.just_entered_pictograph = True
            self.has_entered_pictograph_once = True
            self.remove_same_color_arrow()

        if self.has_entered_pictograph_once:
            self.just_entered_pictograph = False

        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
        new_location = self.pictograph.get_location(scene_pos.x(), scene_pos.y())

        if self.previous_location != new_location and new_location:
            self.previous_location = new_location
            self.update_preview_for_new_location(new_location)
            self.ghost_arrow.update_ghost_arrow(self.attributes)

    ### FLAGS ###

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    ### UPDATERS ###

    def update_prop_during_drag(self) -> None:
        for prop in self.pictograph.prop_set.values():
            if prop.color == self.color:
                if prop not in self.pictograph.props:
                    self.pictograph.props.append(prop)

                prop.set_attributes_from_dict(
                    {
                        COLOR: self.color,
                        PROP_LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                prop.arrow = self.ghost_arrow
                self.ghost_arrow.prop = prop

                if prop not in self.pictograph.items():
                    self.pictograph.addItem(prop)
                prop.show()
                prop.update_appearance()
                self.pictograph.update_props()

    def apply_transformations_to_preview(self) -> None:
        self.update_mirror()
        self.update_rotation()

    def update_mirror(self) -> None:
        if self.is_svg_mirrored:
            transform = QTransform().scale(-1, 1)
            mirrored_pixmap = self.preview.pixmap().transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
            self.preview.setPixmap(mirrored_pixmap)
            self.is_svg_mirrored = True

    def update_rotation(self) -> None:
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.get_rotation_angle(self)

        unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
        unrotated_pixmap = self.preview.pixmap().transformed(unrotate_transform)

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.current_rotation_angle = angle
        self.preview.setPixmap(rotated_pixmap)

        (
            self.start_location,
            self.end_location,
        ) = self.target_arrow.get_start_end_locations(
            self.motion_type,
            self.rotation_direction,
            self.arrow_location,
        )

    def get_rotation_angle(self, arrow: "Arrow") -> RotationAngle:
        motion_type, rotation_direction, color, location = (
            arrow.motion_type,
            arrow.rotation_direction,
            arrow.color,
            arrow.arrow_location,
        )

        rotation_angle_map: Dict[
            Tuple[MotionType, Color],
            Dict[RotationDirection, Dict[Location, RotationAngle]],
        ] = {
            (PRO, RED): {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 0,
                    SOUTHWEST: 90,
                    NORTHWEST: 180,
                },
            },
            (PRO, BLUE): {
                CLOCKWISE: {
                    NORTHEAST: 180,
                    SOUTHEAST: 270,
                    SOUTHWEST: 0,
                    NORTHWEST: 90,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
            },
            (ANTI, RED): {
                CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 0,
                    SOUTHWEST: 90,
                    NORTHWEST: 180,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            },
            (ANTI, BLUE): {
                CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 180,
                    SOUTHEAST: 270,
                    SOUTHWEST: 0,
                    NORTHWEST: 90,
                },
            },
        }

        direction_map: Dict[
            RotationDirection, Dict[Location, RotationAngle]
        ] = rotation_angle_map.get((motion_type, color), {})
        location_map: Dict[Location, RotationAngle] = direction_map.get(
            rotation_direction, {}
        )
        rotation_angle: RotationAngle = location_map.get(location, 0)

        return rotation_angle

    def update_preview_for_new_location(self, new_location: Location) -> None:
        self.arrow_location = new_location
        (
            self.start_location,
            self.end_location,
        ) = self.target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.arrow_location
        )

        self.ghost_arrow.color = self.color
        self.ghost_arrow.arrow_location = new_location
        self.ghost_arrow.motion_type = self.motion_type
        self.ghost_arrow.rotation_direction = self.rotation_direction
        self.ghost_arrow.start_location = self.start_location
        self.ghost_arrow.end_location = self.end_location
        self.ghost_arrow.turns = self.turns
        self.ghost_arrow.is_svg_mirrored = self.is_svg_mirrored

        ghost_svg = self.ghost_arrow.get_svg_file(self.motion_type, self.turns)

        self.ghost_arrow.update_mirror()
        self.ghost_arrow.update_svg(ghost_svg)

        self.update_rotation()
        self.update_prop_during_drag()

        self.pictograph.add_motion(
            self.ghost_arrow,
            self.ghost_arrow.prop,
            IN,
            1,
        )

        if self.ghost_arrow not in self.pictograph.arrows:
            self.pictograph.arrows.append(self.ghost_arrow)
        if self.ghost_arrow not in self.pictograph.items():
            self.pictograph.addItem(self.ghost_arrow)
        self.pictograph.update_pictograph()
