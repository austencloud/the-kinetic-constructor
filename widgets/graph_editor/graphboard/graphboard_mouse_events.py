
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QTransform, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsItem, QToolTip
from objects.staff.staff import Staff
from objects.arrow.arrow import Arrow

from constants import GRAPHBOARD_SCALE, STATIC, PRO, ANTI


class GraphboardMouseEvents():
    def __init__(self, graphboard_view):
        self.view = graphboard_view


    ### MOUSE PRESS ###

    def handle_mouse_press(self, event):
        self.view.setFocus()
        items = self.view.items(event.pos())
        self.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.view.clear_selection()

    def select_or_deselect_items(self, event, items):
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.view.clear_selection()
                items[0].setSelected(True)


    ### DRAG MOVE ###

    def get_current_quadrant(self, event):
        return self.view.get_graphboard_quadrants(self.view.mapToScene(event.position().toPoint()))

    def create_temp_arrow_dict(self, event, current_quadrant):
        dropped_svg = event.mimeData().text()
        base_name = os.path.basename(dropped_svg)
        motion_type = base_name.split('_')[0]
        turns = base_name.split('_')[1].split('.')[0]
        rotation_direction = 'r' if motion_type == PRO else 'l'
        color = event.mimeData().data("color").data().decode()
        temp_arrow_dict = {
            'color': color,
            'motion_type': motion_type,
            'rotation_direction': rotation_direction,
            'quadrant': current_quadrant,
            'start_location': None,
            'end_location': None,
            'turns': turns
        }
        return temp_arrow_dict

    def update_temp_arrow_and_staff(self, current_quadrant, temp_arrow_dict):
        if self.view.temp_arrow is None:
            self.view.temp_arrow = self.view.arrow_factory.create_arrow(self.view, temp_arrow_dict)
            self.view.temp_arrow.color = temp_arrow_dict['color']
            self.view.temp_arrow.start_location, self.view.temp_arrow.end_location = self.view.temp_arrow.attributes.get_start_end_locations(
                temp_arrow_dict['motion_type'], temp_arrow_dict['rotation_direction'], current_quadrant)

            temp_staff_dict = {
                'color': temp_arrow_dict['color'],
                'location': self.view.temp_arrow.end_location,
                'layer': 1
            }
            self.view.temp_staff = self.view.staff_factory.create_staff(self.view.graphboard_scene, temp_staff_dict)
            self.view.graphboard_scene.addItem(self.view.temp_staff)
            self.view.temp_staff.setPos(self.view.staff_xy_locations[self.view.temp_arrow.end_location])
            self.view.temp_staff.is_temporary = True


        self.view.update_dragged_arrow_and_staff(current_quadrant, self.view.temp_arrow, self.view.temp_staff)

    def update_drag_preview(self, current_quadrant):
        new_svg_data = self.view.temp_arrow.set_svg_color(self.view.temp_arrow.svg_file, self.view.temp_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.view.temp_arrow.get_rotation_angle(current_quadrant)
        transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(transform)

        if self.view.drag_preview is not None:
            self.view.drag_preview.setPixmap(rotated_pixmap)
            self.view.drag_preview.setHotSpot(rotated_pixmap.rect().center())


    ### DROP ###

    def handle_drop_event(self, event):
        self.view.setFocus()
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()

        dropped_data = self.extract_dropped_data(event)
        dropped_arrow_dict, dropped_staff_dict = self.create_dropped_dicts(dropped_data)

        arrow, staff = self.handle_existing_items(dropped_data, dropped_arrow_dict, dropped_staff_dict)

        if arrow:
            self.finalize_drop(arrow, staff)

    def extract_dropped_data(self, event):
        dropped_arrow_svg_path = event.mimeData().text()
        dropped_arrow_color = event.mimeData().data("color").data().decode()
        parts = os.path.basename(dropped_arrow_svg_path).split('_')
        dropped_arrow_svg_motion_type = parts[0]
        dropped_arrow_turns = parts[1].split('.')[0]

        if dropped_arrow_svg_motion_type == PRO:
            dropped_arrow_rotation_direction = 'r'
        elif dropped_arrow_svg_motion_type == ANTI:
            dropped_arrow_rotation_direction = 'l'

        self.view.mouse_pos = self.view.mapToScene(event.position().toPoint())
        dropped_arrow_quadrant = self.view.get_graphboard_quadrants(self.view.mouse_pos)
        dropped_arrow_start_location, dropped_arrow_end_location = self.view.arrow_manager.arrow_attributes.get_start_end_locations(
            dropped_arrow_svg_motion_type, dropped_arrow_rotation_direction, dropped_arrow_quadrant)

        return {
            'color': dropped_arrow_color,
            'motion_type': dropped_arrow_svg_motion_type,
            'rotation_direction': dropped_arrow_rotation_direction,
            'quadrant': dropped_arrow_quadrant,
            'start_location': dropped_arrow_start_location,
            'end_location': dropped_arrow_end_location,
            'turns': dropped_arrow_turns
        }

    def create_dropped_dicts(self, dropped_data):
        dropped_arrow_dict = self.view.arrow_manager.arrow_attributes.create_arrow_dict(
            dropped_data['color'], dropped_data['motion_type'], dropped_data['rotation_direction'],
            dropped_data['quadrant'], dropped_data['start_location'], dropped_data['end_location'],
            dropped_data['turns'])
        dropped_staff_dict = self.view.staff_manager.staff_attributes.create_staff_dict(
            dropped_data['color'], dropped_data['end_location'], 1)
        return dropped_arrow_dict, dropped_staff_dict

    def handle_existing_items(self, dropped_data, dropped_arrow_dict, dropped_staff_dict):
        existing_arrows = [item for item in self.view.graphboard_scene.items() if
                           isinstance(item, Arrow) and item.color == dropped_data['color']]
        existing_staffs = [item for item in self.view.graphboard_scene.items() if
                           isinstance(item, Staff) and item.color == dropped_data['color']]
        arrow = None
        staff = None

        if not existing_arrows and not existing_staffs:
            arrow = self.view.arrow_factory.create_arrow(self.view, dropped_arrow_dict)
            staff = self.view.staff_factory.create_staff(self.view.graphboard_scene, dropped_staff_dict)
            self.view.graphboard_scene.addItem(arrow)
            self.view.graphboard_scene.addItem(staff)

        elif existing_staffs and existing_staffs[0].type == STATIC:
            existing_staff = existing_staffs[0]
            existing_staff.attributes.update_attributes(existing_staff, dropped_staff_dict)
            existing_staff.setPos(self.view.staff_xy_locations[dropped_data['end_location']])
            arrow = self.view.arrow_factory.create_arrow(self.view, dropped_arrow_dict)
            self.view.graphboard_scene.addItem(arrow)

        elif existing_arrows and existing_staffs:
            QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
            return arrow, staff

        return arrow, staff

    def finalize_drop(self, arrow, staff):
        arrow.setScale(GRAPHBOARD_SCALE)
        staff.setScale(GRAPHBOARD_SCALE)
        self.view.clear_selection()
        arrow.setSelected(True)

        arrow.staff = staff
        staff.arrow = arrow

        self.view.graphboard_scene.removeItem(self.view.temp_staff)

        for arrow in self.view.graphboard_scene.items():
            if isinstance(arrow, Arrow):
                arrow.arrow_manager.arrow_positioner.update_arrow_position(self.view)

        for staff in self.view.graphboard_scene.items():
            if isinstance(staff, Staff):
                staff.setPos(self.view.staff_manager.staff_xy_locations[staff.location])

        self.view.info_manager.update()