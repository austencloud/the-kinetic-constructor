from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *
from objects.arrow.arrow import Arrow

class Drag(QWidget):
    def __init__(self, main_window, graphboard, arrowbox):
        super().__init__()
        self.initialize_dependencies(main_window, graphboard, arrowbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setParent(main_window)

        self.in_graphboard = False
        self.has_entered_graphboard_once = False
        self.current_rotation_angle = 0
        self.previous_quadrant = None
        self.preview = None

        self.reset_drag_state()

    def set_attributes_to_target_arrow(self, target_arrow):
        self.target_arrow = target_arrow
        pixmap = self.create_pixmap(target_arrow)
        self.color = target_arrow.color
        self.motion_type = target_arrow.motion_type
        self.quadrant = target_arrow.quadrant
        self.rotation_direction = target_arrow.rotation_direction
        self.turns = target_arrow.turns
        (
            self.start_location,
            self.end_location,
        ) = target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        self.preview = QLabel(self)
        self.preview.setPixmap(pixmap)
        self.preview.setFixedHeight(pixmap.height())
        self.preview.setPixmap(pixmap)
        self.center = self.rect().center() * GRAPHBOARD_SCALE

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

    def initialize_dependencies(self, main_window, graphboard, arrowbox):
        self.arrowbox = arrowbox
        self.graphboard = graphboard
        self.main_window = main_window

    def init_temp_arrow(self):
        from objects.arrow.arrow import GhostArrow

        temp_attributes = self.target_arrow.create_attributes_from_arrow(self)
        self.temp_arrow = GhostArrow(self.graphboard, temp_attributes)

    def create_pixmap(self, dragged_arrow):
        new_svg_data = dragged_arrow.set_svg_color(
            dragged_arrow.svg_file, dragged_arrow.color
        )
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)
        return pixmap

    def get_attributes(self):
        (
            start_location,
            end_location,
        ) = self.target_arrow.attributes.get_start_end_locations(
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

    def move_to_cursor(self, arrowbox, event_pos):
        local_pos = arrowbox.view.mapTo(self.main_window, event_pos)
        self.move(local_pos - self.center * GRAPHBOARD_SCALE)

    def update_rotation(self):
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.target_arrow.get_rotation_angle(
            self.quadrant,
            self.motion_type,
            self.rotation_direction,
        )

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

    def update_for_graphboard(self, event_pos):
        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        view_pos_in_graphboard = self.graphboard.view.mapFromGlobal(pos_in_main_window)
        scene_pos = self.graphboard.view.mapToScene(view_pos_in_graphboard)

        if not self.has_entered_graphboard_once:
            self.just_entered_graphboard = True
            self.has_entered_graphboard_once = True
            self.init_temp_arrow()

        new_quadrant = self.graphboard.determine_quadrant(scene_pos.x(), scene_pos.y())

        if self.previous_quadrant != new_quadrant:
            self.update_drag_preview_for_new_quadrant(new_quadrant)

    def update_drag_preview_for_new_quadrant(self, new_quadrant):
        for arrow in self.graphboard.arrows[:]:
            if arrow.isVisible() and arrow.color == self.color:
                self.graphboard.removeItem(arrow)
                self.graphboard.arrows.remove(arrow)

        self.quadrant = new_quadrant
        self.update_rotation()
        new_arrow = self.temp_arrow.create_attributes_from_arrow(self)
        self.temp_arrow.update_attributes(new_arrow)
        self.temp_arrow.show()

        # if the temp arrow isn't already in the graphboard, add it to the graphboard
        if self.temp_arrow not in self.graphboard.items():
            self.graphboard.addItem(self.temp_arrow)
            self.graphboard.arrows.append(self.temp_arrow)
            self.graphboard.arrow_positioner.update_arrow_positions()
            self.temp_arrow.update_appearance()

        self.graphboard.update_letter()
        self.previous_quadrant = new_quadrant
        self.quadrant = new_quadrant
        (
            self.start_location,
            self.end_location,
        ) = self.temp_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        self.update_staff_during_drag()

    def update_staff_during_drag(self):
        for staff in self.graphboard.staff_set.values():
            if staff.color == self.color:
                staff.update_attributes(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                staff.arrow = self.temp_arrow
                self.temp_arrow.staff = staff
                staff.show()
                staff.update_appearance()
                if staff not in self.graphboard.staffs:
                    self.graphboard.staffs.append(staff)
                self.graphboard.update_staffs()

    def place_arrow_on_graphboard(self):
        self.graphboard.arrow_positioner.update_arrow_positions()
        self.graphboard.clearSelection()

        self.placed_arrow = Arrow(self.graphboard, self.temp_arrow.get_attributes())
        self.placed_arrow.staff = self.temp_arrow.staff

        self.graphboard.addItem(self.placed_arrow)
        self.graphboard.arrows.append(self.placed_arrow)

        self.graphboard.removeItem(self.temp_arrow)
        self.graphboard.arrows.remove(self.temp_arrow)

        self.placed_arrow.update_appearance()
        self.placed_arrow.show()
        self.placed_arrow.setSelected(True)

        self.graphboard.arrow_positioner.update_arrow_positions()

    def start_drag(self, event_pos):
        self.move_to_cursor(self.arrowbox, event_pos)
        self.show()

    def handle_mouse_move(self, arrowbox, event_pos):
        if self.preview:
            self.move_to_cursor(arrowbox, event_pos)
            if self.is_over_graphboard(arrowbox, event_pos):
                self.update_for_graphboard(event_pos)

    def handle_mouse_release(self, view_pos):
        if (
            view_pos not in self.arrowbox.view.rect()
            and self.has_entered_graphboard_once
        ):
            self.place_arrow_on_graphboard()
        self.deleteLater()
        self.graphboard.update()
        self.arrowbox.drag = None
        self.reset_drag_state()

    def is_over_graphboard(self, arrowbox, event_pos):
        pos_in_main_window = arrowbox.view.mapToGlobal(event_pos)
        local_pos_in_graphboard = self.graphboard.view.mapFromGlobal(pos_in_main_window)

        return self.graphboard.view.rect().contains(local_pos_in_graphboard)
