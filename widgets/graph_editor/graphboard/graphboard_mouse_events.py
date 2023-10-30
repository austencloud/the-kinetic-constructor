
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
        self.scene = self.view.scene()
        self.staff_manager = self.view.staff_manager
        self.staff_factory = self.staff_manager.staff_factory
        self.temp_staff = None
        
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

    def update_temp_staff(self, drag_preview):
        for temp_staff in self.scene.items():
            if isinstance(temp_staff, Staff) and temp_staff.color == drag_preview.color:
                self.scene.removeItem(temp_staff)

        temp_staff_dict = {
            'color': drag_preview.color,
            'location': drag_preview.end_location,
            'layer': 1
        }
        
        self.temp_staff = self.staff_factory.create_staff(self.view.graphboard_scene, temp_staff_dict)
        self.view.temp_staff = self.temp_staff
        self.scene.addItem(self.temp_staff)
        self.temp_staff.setPos(self.staff_manager.staff_xy_locations[drag_preview.end_location])


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