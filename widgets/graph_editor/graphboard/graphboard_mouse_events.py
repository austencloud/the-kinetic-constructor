
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
        self.graphboard_view = graphboard_view
        self.graphboard_scene = self.graphboard_view.scene()
        self.staff_manager = self.graphboard_view.staff_manager
        self.arrow_factory = self.graphboard_view.main_widget.arrow_manager.arrow_factory
        self.staff_factory = self.staff_manager.staff_factory
        self.temp_staff = None
        
    ### MOUSE PRESS ###

    def handle_mouse_press(self, event):
        self.graphboard_view.setFocus()
        items = self.graphboard_view.items(event.pos())
        self.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard_view.clear_selection()

    def select_or_deselect_items(self, event, items):
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.graphboard_view.clear_selection()
                items[0].setSelected(True)


    ### DRAG MOVE ###

    def get_current_quadrant(self, event):
        return self.graphboard_view.get_graphboard_quadrants(self.graphboard_view.mapToScene(event.position().toPoint()))

    def update_temp_staff(self, drag_preview):
        for temp_staff in self.graphboard_scene.items():
            if isinstance(temp_staff, Staff) and temp_staff.color == drag_preview.color:
                self.graphboard_scene.removeItem(temp_staff)

        temp_staff_dict = {
            'color': drag_preview.color,
            'location': drag_preview.end_location,
            'layer': 1
        }
        
        self.temp_staff = self.staff_factory.create_staff(self.graphboard_view.graphboard_scene, temp_staff_dict)
        self.graphboard_view.temp_staff = self.temp_staff
        self.graphboard_scene.addItem(self.temp_staff)
        self.temp_staff.setPos(self.staff_manager.staff_xy_locations[drag_preview.end_location])


    ### DROP ###

    def handle_drop_event(self, event, drag_preview):
        self.graphboard_view.setFocus()
        event.accept()

        new_arrow_dict = {
            'color': drag_preview.color,
            'motion_type': drag_preview.motion_type,
            'rotation_direction': drag_preview.rotation_direction,
            'quadrant': drag_preview.quadrant,
            'start_location': drag_preview.start_location,
            'end_location': drag_preview.end_location,
            'turns': drag_preview.turns
        }
        
        new_staff_dict = {
            'color': drag_preview.color,
            'location': drag_preview.end_location,
            'layer': 1
        }

        new_arrow = self.arrow_factory.create_arrow(self.graphboard_view, new_arrow_dict)
        new_staff = self.staff_factory.create_staff(self.graphboard_scene, new_staff_dict)

        #make the arrow movable
        new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard_view.clear_selection()
        
        new_arrow.setSelected(True)

        new_arrow.staff = new_staff
        new_staff.arrow = new_arrow

        self.graphboard_scene.addItem(new_arrow)
        self.graphboard_scene.addItem(new_staff)

        self.graphboard_scene.removeItem(self.graphboard_view.temp_staff)
        
        drag_preview.hide()
        
        for arrow in self.graphboard_view.graphboard_scene.items():
            if isinstance(arrow, Arrow):
                arrow.arrow_manager.arrow_positioner.update_arrow_position(self.graphboard_view)

        for staff in self.graphboard_view.graphboard_scene.items():
            if isinstance(staff, Staff):
                staff.setPos(self.graphboard_view.staff_manager.staff_xy_locations[staff.location])

        self.graphboard_view.info_manager.update()

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

        self.graphboard_view.mouse_pos = self.graphboard_view.mapToScene(event.position().toPoint())
        dropped_arrow_quadrant = self.graphboard_view.get_graphboard_quadrants(self.graphboard_view.mouse_pos)
        dropped_arrow_start_location, dropped_arrow_end_location = self.graphboard_view.arrow_manager.arrow_attributes.get_start_end_locations(
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
        dropped_arrow_dict = self.arrow_manager.arrow_attributes.create_arrow_dict(
            dropped_data['color'], dropped_data['motion_type'], dropped_data['rotation_direction'],
            dropped_data['quadrant'], dropped_data['start_location'], dropped_data['end_location'],
            dropped_data['turns'])
        dropped_staff_dict = self.staff_manager.staff_attributes.create_staff_dict(
            dropped_data['color'], dropped_data['end_location'], 1)
        return dropped_arrow_dict, dropped_staff_dict

    def handle_existing_items(self, dropped_data, dropped_arrow_dict, dropped_staff_dict):
        existing_arrows = [item for item in self.graphboard_scene.items() if
                           isinstance(item, Arrow) and item.color == dropped_data['color']]
        existing_staffs = [item for item in self.graphboard_scene.items() if
                           isinstance(item, Staff) and item.color == dropped_data['color']]
        arrow = None
        staff = None

        if not existing_arrows and not existing_staffs:
            arrow = self.arrow_factory.create_arrow(self.graphboard_view, dropped_arrow_dict)
            staff = self.staff_factory.create_staff(self.graphboard_scene, dropped_staff_dict)
            self.graphboard_scene.addItem(arrow)
            self.graphboard_scene.addItem(staff)

        elif existing_staffs and existing_staffs[0].type == STATIC:
            existing_staff = existing_staffs[0]
            existing_staff.attributes.update_attributes(existing_staff, dropped_staff_dict)
            existing_staff.setPos(self.graphboard_view.staff_xy_locations[dropped_data['end_location']])
            arrow = self.arrow_factory.create_arrow(self.graphboard_view, dropped_arrow_dict)
            self.graphboard_scene.addItem(arrow)

        elif existing_arrows and existing_staffs:
            QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
            return arrow, staff

        return arrow, staff

