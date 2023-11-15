from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import (
    COLOR,
    MOTION_TYPE,
    QUADRANT,
    ROTATION_DIRECTION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    LOCATION,
    LAYER,
)
from objects.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graphboard.graphboard import GraphBoard
    from widgets.arrowbox.arrowbox import ArrowBox
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    Color,
    MotionType,
    Quadrant,
    RotationDirection,
    Location,
    Turns,
)


class ArrowBoxDrag(QWidget):
    color: Color
    motion_type: MotionType
    quadrant: Quadrant
    rotation_direction: RotationDirection
    start_location: Location
    end_location: Location
    turns: Turns

    def __init__(
        self, main_window: "MainWindow", graphboard: "GraphBoard", arrowbox: "ArrowBox"
    ) -> None:
        super().__init__()
        self.setParent(main_window)
        self.setup_dependencies(main_window, graphboard, arrowbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.attributes: ArrowAttributesDicts = {}
        self.reset_drag_state()

        self.last_update_time = 0
        self.update_interval = 0.1

    def setup_dependencies(
        self, main_window: "MainWindow", graphboard: "GraphBoard", arrowbox: "ArrowBox"
    ) -> None:
        self.arrowbox = arrowbox
        self.graphboard = graphboard
        self.main_window = main_window

        self.has_entered_graphboard_once = False
        self.current_rotation_angle = 0
        self.previous_quadrant = None
        self.preview = None
        self.svg_file = None
        self.ghost_arrow = None

    def match_target_arrow(self, target_arrow: "Arrow") -> None:
        self.target_arrow = target_arrow
        self.set_attributes(target_arrow)
        pixmap = self.create_pixmap(target_arrow)
        self.preview.setPixmap(pixmap)
        self.preview.setFixedHeight(pixmap.height())
        self.arrow_center = self.target_arrow.boundingRect().center() * GRAPHBOARD_SCALE

    def set_attributes(self, target_arrow: "Arrow") -> None:
        for attribute_name in target_arrow.attributes.keys():
            setattr(
                self, attribute_name.lower(), target_arrow.attributes[attribute_name]
            )
        (
            self.start_location,
            self.end_location,
        ) = target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        self.ghost_arrow = self.graphboard.ghost_arrows[self.color]
        self.ghost_arrow.target_arrow = target_arrow

    def reset_drag_state(self) -> None:
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

    def create_pixmap(self, target_arrow: "Arrow") -> QPixmap:
        new_svg_data = target_arrow.set_svg_color(target_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
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
            self.motion_type, self.rotation_direction, self.quadrant
        )

        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: self.quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: start_location,
            END_LOCATION: end_location,
            TURNS: self.turns,
        }

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.arrowbox.view.mapTo(self.main_window, event_pos)
        self.move(local_pos - (self.arrow_center).toPoint())

    def remove_same_color_arrow(self) -> None:
        for arrow in self.graphboard.arrows[:]:
            if arrow.isVisible() and arrow.color == self.color:
                self.graphboard.removeItem(arrow)
                self.graphboard.arrows.remove(arrow)
        for staff in self.graphboard.staffs[:]:
            if staff.isVisible() and staff.color == self.color:
                self.graphboard.removeItem(staff)
                self.graphboard.staffs.remove(staff)

    def place_arrow_on_graphboard(self) -> None:
        self.graphboard.update()
        self.graphboard.clearSelection()

        self.placed_arrow = Arrow(self.graphboard, self.ghost_arrow.get_attributes())
        self.placed_arrow.staff = self.ghost_arrow.staff
        self.ghost_arrow.staff.arrow = self.placed_arrow

        self.graphboard.addItem(self.placed_arrow)
        self.graphboard.arrows.append(self.placed_arrow)

        self.graphboard.removeItem(self.ghost_arrow)
        self.graphboard.arrows.remove(self.ghost_arrow)

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
            if self.is_over_graphboard(event_pos):
                self.handle_enter_graphboard(event_pos)

    def handle_mouse_release(self) -> None:
        if self.has_entered_graphboard_once:
            self.place_arrow_on_graphboard()
        self.deleteLater()
        self.graphboard.update()
        self.arrowbox.arrowbox_drag = None
        self.ghost_arrow.staff = None
        self.reset_drag_state()

    ### FLAGS ###

    def is_over_graphboard(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        local_pos_in_graphboard = self.graphboard.view.mapFromGlobal(pos_in_main_window)
        return self.graphboard.view.rect().contains(local_pos_in_graphboard)

    ### UPDATERS ###

    def update_staff_during_drag(self) -> None:
        for staff in self.graphboard.staff_set.values():
            if staff.color == self.color:
                if staff not in self.graphboard.staffs:
                    self.graphboard.staffs.append(staff)

                staff.set_attributes_from_dict(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                staff.arrow = self.ghost_arrow
                self.ghost_arrow.staff = staff
                if staff not in self.graphboard.items():
                    self.graphboard.addItem(staff)
                staff.show()
                staff.update_appearance()
                self.graphboard.update_staffs()

    def update_rotation(self) -> None:
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.target_arrow.get_rotation_angle(self)

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
            self.quadrant,
        )

    def handle_enter_graphboard(self, event_pos: QPoint) -> None:
        if not self.has_entered_graphboard_once:
            self.just_entered_graphboard = True
            self.has_entered_graphboard_once = True
            self.remove_same_color_arrow()

        if self.has_entered_graphboard_once:
            self.just_entered_graphboard = False

        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        view_pos_in_graphboard = self.graphboard.view.mapFromGlobal(pos_in_main_window)
        scene_pos = self.graphboard.view.mapToScene(view_pos_in_graphboard)
        new_quadrant = self.graphboard.get_quadrant(scene_pos.x(), scene_pos.y())

        if self.previous_quadrant != new_quadrant and new_quadrant:
            self.previous_quadrant = new_quadrant
            self.update_preview_for_new_quadrant(new_quadrant)
            self.ghost_arrow.update(self.attributes)
            self.ghost_arrow.attributes = self.attributes

    def update_preview_for_new_quadrant(self, new_quadrant: Quadrant) -> None:
        self.quadrant = new_quadrant
        (
            self.start_location,
            self.end_location,
        ) = self.target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        self.attributes[COLOR] = self.color
        self.attributes[MOTION_TYPE] = self.motion_type
        self.attributes[QUADRANT] = new_quadrant
        self.attributes[ROTATION_DIRECTION] = self.rotation_direction
        self.attributes[START_LOCATION] = self.start_location
        self.attributes[END_LOCATION] = self.end_location
        self.attributes[TURNS] = self.turns

        if self.ghost_arrow.is_mirrored:
            self.ghost_arrow.is_mirrored = False
            self.ghost_arrow.mirror()

        self.ghost_arrow.quadrant = new_quadrant
        self.update_rotation()
        self.ghost_arrow.update(self.attributes)

        self.update_staff_during_drag()

        if self.ghost_arrow not in self.graphboard.arrows:
            self.graphboard.arrows.append(self.ghost_arrow)
        if self.ghost_arrow not in self.graphboard.items():
            self.graphboard.addItem(self.ghost_arrow)
        self.graphboard.update()
