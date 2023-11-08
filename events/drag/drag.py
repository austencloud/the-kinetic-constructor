from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *


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
    
        self.init_invisible_arrow()
        self.reset_drag_state()

    def set_attributes_to_target_arrow(self, target_arrow):
        self.target_arrow = target_arrow
        pixmap = self.create_pixmap(target_arrow)
        self.center = pixmap.rect().center() * GRAPHBOARD_SCALE
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

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0


    def initialize_dependencies(self, main_window, graphboard, arrowbox):
        self.arrowbox = arrowbox
        self.graphboard = graphboard
        self.main_window = main_window

    def init_invisible_arrow(self):
        from objects.arrow.arrow import Arrow
        self.invisible_arrow = Arrow(self.graphboard, None)
        self.invisible_arrow.hide()
        self.graphboard.addItem(self.invisible_arrow)

    def update(self, event_pos):

        self.update_drag_preview_for_graphboard(event_pos)
            
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

    def update_rotation_for_quadrant(self, new_quadrant):
        self.in_graphboard = True
        self.quadrant = new_quadrant
        self.update_rotation()

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


    def update_drag_preview_for_graphboard(self, event_pos):
        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        view_pos_in_graphboard = self.graphboard.view.mapFromGlobal(pos_in_main_window)
        scene_pos = self.graphboard.view.mapToScene(view_pos_in_graphboard)
        
        if not self.has_entered_graphboard_once:
            self.just_entered_graphboard = True
            self.has_entered_graphboard_once = True

        new_quadrant = self.graphboard.determine_quadrant(
            scene_pos.x(), scene_pos.y()
        )

        if self.previous_quadrant != new_quadrant:
            self.update_drag_preview_for_new_quadrant(new_quadrant)

    def update_drag_preview_for_new_quadrant(self, new_quadrant):
        for arrow in self.graphboard.arrows[
            :
        ]:  # Copy the list to avoid iteration issues
            if arrow.color == self.color:
                self.graphboard.removeItem(arrow)
                self.graphboard.arrows.remove(arrow)

        self.update_rotation_for_quadrant(new_quadrant)
        new_arrow = self.invisible_arrow.create_dict_from_arrow(self)
        self.invisible_arrow.update_attributes(new_arrow)
        self.previous_quadrant = new_quadrant
        self.quadrant = new_quadrant
        self.start_location, self.end_location = self.invisible_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        self.update_staffs()

    def update_staffs(self):
        for staff in [self.graphboard.red_staff, self.graphboard.blue_staff]:
            if staff.color == self.color:
                staff.update_attributes(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                staff.arrow = self.invisible_arrow
                self.invisible_arrow.staff = staff
                staff.show()
                self.graphboard.staffs.append(staff)
                staff.update_appearance()
                self.graphboard.update_staffs()

    def place_arrow_on_graphboard(self):
        self.invisible_arrow.show()
        self.graphboard.clearSelection()
        self.invisible_arrow.setSelected(True)
        self.graphboard.arrows.append(self.invisible_arrow) 
        
    def start_drag(self, event_pos):
        self.move_to_cursor(self.arrowbox, event_pos)
        self.show()

    def handle_mouse_move(self, arrowbox, event_pos):
        self.move_to_cursor(arrowbox, event_pos)
        self.update(event_pos)

    def handle_mouse_release(self, view_pos):
        if view_pos not in self.arrowbox.view.rect():
            self.place_arrow_on_graphboard()
        self.deleteLater()
        self.graphboard.update()
        self.arrowbox.drag = None
        self.reset_drag_state()

    def is_over_graphboard(self, arrowbox, event_pos):
        # the event position is in the arorowbox view. Convert it to the coordinates of the main window. 
        pos_in_main_window = arrowbox.view.mapTo(self.main_window, event_pos)
        
        local_pos_in_graphboard = self.graphboard.view.mapFrom(
            arrowbox.main_widget, pos_in_main_window
        )
        return self.graphboard.view.rect().contains(local_pos_in_graphboard)

