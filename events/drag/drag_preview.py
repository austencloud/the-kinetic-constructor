from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from resources.constants.constants import GRAPHBOARD_SCALE


class DragPreview(QWidget):
    def __init__(self, drag_manager, arrow):
        super().__init__()

        self.drag_manager = drag_manager
        self.arrow = arrow
        pixmap = self.create_pixmap(arrow)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(pixmap.height())
        self.label.setPixmap(pixmap)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.center = pixmap.rect().center() * GRAPHBOARD_SCALE

        self.color = arrow.color
        self.motion_type = arrow.motion_type
        self.quadrant = arrow.quadrant
        self.rotation_direction = arrow.rotation_direction
        self.turns = arrow.turns

        (
            self.start_location,
            self.end_location,
        ) = arrow.attributes.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        self.in_graphboard = False
        self.has_entered_graphboard_once = False
        self.current_rotation_angle = 0

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
        start_location, end_location = self.arrow.attributes.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: self.quadrant,
            ROT_DIR: self.rotation_direction,
            START: start_location,
            END: end_location,
            TURNS: self.turns,
        }

    def move_to_cursor(self, view, event, target_arrow):
        main_window = view.window()
        local_pos = view.mapTo(main_window, event.pos())
        self.move(local_pos - (target_arrow.center * GRAPHBOARD_SCALE).toPoint())

    def update_rotation_for_quadrant(self, new_quadrant):
        self.in_graphboard = True
        self.quadrant = new_quadrant
        self.rotate()

    def rotate(self):
        renderer = QSvgRenderer(self.drag_manager.event_handler.target_arrow.svg_file)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.drag_manager.event_handler.target_arrow.get_rotation_angle(
            self.quadrant,
            self.motion_type,
            self.rotation_direction,
        )

        unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
        unrotated_pixmap = self.label.pixmap().transformed(unrotate_transform)

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.current_rotation_angle = angle
        self.label.setPixmap(rotated_pixmap)

        (
            self.start_location,
            self.end_location,
        ) = self.drag_manager.event_handler.target_arrow.attributes.get_start_end_locations(
            self.motion_type,
            self.rotation_direction,
            self.quadrant,
        )

    def delete(self):
        self.deleteLater()
        self = None
