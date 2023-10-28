
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
    
    def mousePressEvent(self, event):
        self.view.setFocus()
        items = self.view.items(event.pos())
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if event.button() == Qt.MouseButton.LeftButton and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.view.clear_selection()
                items[0].setSelected(True)
        else:
            self.view.clear_selection()
        super().mousePressEvent(event)
        
        # Check if any item got selected after calling the parent class's method
        if items and not items[0].isSelected():
            items[0].setSelected(True)

    def dragMoveEvent(self, event):
        current_quadrant = self.view.get_graphboard_quadrants(self.view.mapToScene(event.position().toPoint()))  # Changed event.pos() to event.position()

        dropped_svg = event.mimeData().text()
        base_name = os.path.basename(dropped_svg)
        motion_type = base_name.split('_')[0]
        turns = base_name.split('_')[1].split('.')[0]
        rotation_direction = 'r' if motion_type == PRO else 'l'
        color = event.mimeData().data("color").data().decode()  # Retrieve the color
        for arrow in self.view.scene().items():
            if isinstance(arrow, Arrow):
                if arrow.color == color:
                    event.ignore()
                    QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
                    return
        event.accept()
        QToolTip.hideText() 
        
        temp_arrow_dict = {
            'color': color,
            'motion_type': motion_type,
            'rotation_direction': rotation_direction,
            'quadrant': current_quadrant,
            'start_location': None,
            'end_location': None,
            'turns': turns
        }
        
        if self.view.temp_arrow is None:
            self.view.temp_arrow = self.view.arrow_factory.create_arrow(self.view, temp_arrow_dict)
            self.view.temp_arrow.color = event.mimeData().data("color").data().decode() 
            self.view.temp_arrow.start_location, self.view.temp_arrow.end_location = self.view.temp_arrow.attributes.get_start_end_locations(motion_type, rotation_direction, current_quadrant)
           
            temp_staff_dict = {
                'color': color,
                'location': self.view.temp_arrow.end_location,
                'layer': 1
            } 
        

            self.view.temp_staff = self.view.staff_factory.create_staff(self.view.graphboard_scene, temp_staff_dict)
            self.view.graphboard_scene.addItem(self.view.temp_staff)
            
    
        # Update the temporary arrow and staff
        self.view.update_dragged_arrow_and_staff(current_quadrant, self.view.temp_arrow, self.view.temp_staff)

        # Update the pixmap based on the new quadrant
        new_svg_data = self.view.temp_arrow.set_svg_color(self.view.temp_arrow.svg_file, self.view.temp_arrow.color)
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE  # Scale the pixmap
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)
        
        # Apply rotation to the pixmap
        angle = self.view.temp_arrow.get_rotation_angle(current_quadrant)
        transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(transform)
        
        if self.view.drag_preview is not None:
            # Update the drag's pixmap
            self.view.drag_preview.setPixmap(rotated_pixmap)
            self.view.drag_preview.setHotSpot(rotated_pixmap.rect().center())

    def update_dragged_arrow_and_staff(self, current_quadrant, temp_arrow, temp_staff):
        temp_arrow.quadrant = current_quadrant
        temp_arrow.update_rotation()
        temp_arrow.update_appearance()
        temp_arrow.start_location, temp_arrow.end_location = temp_arrow.attributes.get_start_end_locations(
            temp_arrow.motion_type, temp_arrow.rotation_direction, current_quadrant)
        temp_staff_dict = {
            'color': temp_arrow.color,
            'location': temp_arrow.end_location,
            'layer': 1
        }
        temp_staff.attributes.update_attributes(temp_staff, temp_staff_dict)
        temp_staff.update_appearance()
        temp_staff.setPos(self.view.staff_manager.staff_xy_locations[temp_staff_dict['location']])

    def dropEvent(self, event):
        arrow = None
        self.view.setFocus()
        event.setDropAction(Qt.DropAction.CopyAction)
        event.accept()
        dropped_arrow_svg_path = event.mimeData().text()
        dropped_arrow_color = event.mimeData().data("color").data().decode()  # Retrieve the color
        parts = os.path.basename(dropped_arrow_svg_path).split('_')
        dropped_arrow_svg_motion_type = parts[0]
        dropped_arrow_turns = parts[1].split('.')[0]
        
        if dropped_arrow_svg_motion_type == PRO:
            dropped_arrow_rotation_direction = 'r'
        elif dropped_arrow_svg_motion_type == ANTI:
            dropped_arrow_rotation_direction = 'l'
            
        self.view.mouse_pos = self.view.mapToScene(event.position().toPoint()) 
        dropped_arrow_quadrant = self.view.get_graphboard_quadrants(self.view.mouse_pos)
        dropped_arrow_start_location, dropped_arrow_end_location = self.view.arrow_manager.arrow_attributes.get_start_end_locations(dropped_arrow_svg_motion_type, dropped_arrow_rotation_direction, dropped_arrow_quadrant)
        
        # Create the dropped arrow/staff dictionaries
        dropped_arrow_dict = self.view.arrow_manager.arrow_attributes.create_arrow_dict(dropped_arrow_color, dropped_arrow_svg_motion_type, dropped_arrow_rotation_direction, dropped_arrow_quadrant, dropped_arrow_start_location, dropped_arrow_end_location, dropped_arrow_turns)
        dropped_staff_dict = self.view.staff_manager.staff_attributes.create_staff_dict(dropped_arrow_color, dropped_arrow_end_location, 1)
        
        # Check for existing arrows and staffs of the same color
        existing_arrows = [item for item in self.view.graphboard_scene.items() if isinstance(item, Arrow) and item.color == dropped_arrow_color]
        existing_staffs = [item for item in self.view.graphboard_scene.items() if isinstance(item, Staff) and item.color == dropped_arrow_color]

        # Case 1: No existing staff or arrow of the same color
        if not existing_arrows and not existing_staffs:
            arrow = self.view.arrow_factory.create_arrow(self.view, dropped_arrow_dict)
            staff = self.view.staff_factory.create_staff(self.view.graphboard_scene, dropped_staff_dict)
            self.view.graphboard_scene.addItem(arrow)
            self.view.graphboard_scene.addItem(staff)

        # Case 2: Existing staff of the same color but is static
        elif existing_staffs and existing_staffs[0].type == STATIC:
            existing_staff = existing_staffs[0]
            existing_staff.attributes.update_attributes(existing_staff, dropped_staff_dict)  # Update the staff's attributes
            existing_staff.setPos(self.view.staff_xy_locations[dropped_arrow_end_location])  # Update staff position
            arrow = self.view.arrow_factory.create_arrow(self.view, dropped_arrow_dict)
            self.view.graphboard_scene.addItem(arrow)

        # Case 3: Both existing staff and arrow of the same color
        elif existing_arrows and existing_staffs:
            event.ignore()
            QToolTip.showText(QCursor.pos(), "Cannot add two motions of the same color.")
            return
        
        if arrow: 
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
