
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QGraphicsItem, QToolTip
from objects.staff.staff import Staff
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from constants import STATIC


class GraphboardMouseEvents():
    def __init__(self, graphboard_view):
        self.graphboard_view = graphboard_view
        self.graphboard_scene = self.graphboard_view.scene()
        self.staff_handler = self.graphboard_view.staff_handler
        self.arrow_factory = self.graphboard_view.main_widget.arrow_manager.arrow_factory
        self.staff_factory = self.staff_handler.staff_factory
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
        if self.graphboard_view.temp_staff:
            self.prev_staff_state = {
                'color': self.graphboard_view.temp_staff.color,
                'location': self.graphboard_view.temp_staff.location,
                'layer': self.graphboard_view.temp_staff.layer
            }
        
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
        self.temp_staff.setPos(self.staff_handler.staff_xy_locations[drag_preview.end_location])


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
        
        for item in self.graphboard_view.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.arrow_manager.arrow_positioner.update_arrow_position(self.graphboard_view)

        for item in self.graphboard_view.graphboard_scene.items():
            if isinstance(item, Staff):
                item.setPos(self.graphboard_view.staff_handler.staff_xy_locations[item.location])

        self.graphboard_view.info_handler.update()


