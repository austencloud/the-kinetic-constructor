from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *
from objects.arrow.arrow import Arrow
from widgets.graph_editor.graphboard.object_manager.ghost_arrow_manager import (
    GhostArrowManager,
)


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

        self.ghost_arrow_manager = self.graphboard.ghost_arrow_manager
        self.ghost_arrow = self.ghost_arrow_manager.init_ghost_arrow()

        self.reset_drag_state()

    def set_attributes_to_target_arrow(self, target_arrow):
        self.target_arrow = target_arrow
        self.ghost_arrow.target_arrow = target_arrow
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

    def create_pixmap(self, target_arrow):
        new_svg_data = target_arrow.set_svg_color(
            target_arrow.svg_file, target_arrow.color
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
            self.remove_same_color_arrow()

        new_quadrant = self.graphboard.determine_quadrant(scene_pos.x(), scene_pos.y())

        if self.previous_quadrant != new_quadrant:
            self.update_drag_preview_for_new_quadrant(new_quadrant)
            new_quadrant = self.previous_quadrant
            self.graphboard.arrow_positioner.update_arrow_positions()


    def update_drag_preview_for_new_quadrant(self, new_quadrant):
        self.quadrant = new_quadrant
        self.update_rotation()
        self.ghost_arrow_manager.update_ghost_arrow(new_quadrant, self)
        self.graphboard.arrow_positioner.update_arrow_positions()

        self.update_staff_during_drag()
        if self.ghost_arrow not in self.graphboard.arrows:
            self.graphboard.arrows.append(self.ghost_arrow)
        if self.ghost_arrow not in self.graphboard.items():
            self.graphboard.addItem(self.ghost_arrow)
        self.graphboard.update_letter()
        self.graphboard.update_staffs()



    def remove_same_color_arrow(self):
        for arrow in self.graphboard.arrows[:]:
            if arrow.isVisible() and arrow.color == self.color:
                self.graphboard.removeItem(arrow)
                self.graphboard.arrows.remove(arrow)
        for staff in self.graphboard.staffs[:]:
            if staff.isVisible() and staff.color == self.color:
                self.graphboard.removeItem(staff)
                self.graphboard.staffs.remove(staff)

    def update_staff_during_drag(self):
        for staff in self.graphboard.staff_set.values():
            if staff.color == self.color:
                if staff not in self.graphboard.staffs:
                    self.graphboard.staffs.append(staff)

                staff.update_attributes(
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

    def place_arrow_on_graphboard(self):
        self.graphboard.arrow_positioner.update_arrow_positions()
        self.graphboard.clearSelection()

        self.placed_arrow = Arrow(self.graphboard, self.ghost_arrow.get_attributes())
        self.placed_arrow.staff = self.ghost_arrow.staff

        self.graphboard.addItem(self.placed_arrow)
        self.graphboard.arrows.append(self.placed_arrow)

        self.graphboard.removeItem(self.ghost_arrow)
        self.graphboard.arrows.remove(self.ghost_arrow)

        self.placed_arrow.update_appearance()
        self.placed_arrow.show()
        self.placed_arrow.setSelected(True)

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
