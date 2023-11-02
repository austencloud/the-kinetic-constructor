from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem, QApplication
from PyQt6.QtGui import QCursor, QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from resources.constants import GRAPHBOARD_SCALE, STATIC
from events.drag.drag_preview import DragPreview
from objects.staff.staff import Staff
from events.drag.drag_helpers import DragHelpers
from events.drag.drag_scene_updater import SceneUpdater
from events.drag.drag_event_handler import DragEventHandler


class DragManager:
    ### INITIALIZATION ###

    def __init__(self):
        self.reset_drag_state()


    def initialize_dependencies(self, graphboard_view, arrowbox_view):
        self.graphboard_view = graphboard_view
        self.arrowbox_view = arrowbox_view
        self.graphboard_scene = self.graphboard_view.scene()
        self.arrow_factory = (
            self.graphboard_view.main_widget.arrow_manager.arrow_factory
        )
        self.info_handler = self.graphboard_view.info_handler
        self.staff_handler = self.graphboard_view.staff_handler
        self.staff_factory = self.graphboard_view.staff_handler.staff_factory

        self.helpers = DragHelpers(self)
        self.event_handler = DragEventHandler(self)
        self.scene_updater = SceneUpdater(self)

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0
        self.has_entered_graphboard_once = False
        self.invisible_arrow = None  # Reset the invisible arrow



    ### OBJECT CREATION AND UPDATE ###


    def create_and_add_arrow(self, arrow_dict):
        new_arrow = self.arrow_factory.create_arrow(self.graphboard_view, arrow_dict)
        new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard_scene.addItem(new_arrow)
        return new_arrow

    def create_and_add_staff(self, staff_dict):
        new_staff = self.staff_factory.create_staff(self.graphboard_scene, staff_dict)

        for staff in self.staff_handler.staffs_on_board:
            if staff.color == new_staff.color:
                self.staff_handler.staffs_on_board.remove(staff)

        self.staff_handler.staffs_on_board.append(new_staff)

        return new_staff

    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow

    def get_current_quadrant(self, event):
        return self.graphboard_view.get_graphboard_quadrants(
            self.graphboard_view.mapToScene(event.position().toPoint())
        )

    def update_staff(self, drag_preview):
        if not self.arrow_dragged:
            return

        for staff in self.graphboard_scene.items():
            if isinstance(staff, Staff) and staff.color == drag_preview.color:
                self.graphboard_scene.removeItem(staff)

        staff_dict = self.create_staff_dict_from_drag_preview()
        new_staff = self.create_and_add_staff(staff_dict)
        
        self.staff = new_staff
        self.graphboard_scene.addItem(self.staff)
        
        for item in self.graphboard_scene.items():
            from objects.arrow.arrow import Arrow
            if isinstance(item, Arrow) and item.color == new_staff.color:
                self.staff.arrow = item
                item.staff = self.staff
                return
        
        self.staff.setPos(
            self.staff_handler.staff_xy_locations[drag_preview.end_location]
        )
        self.drag_preview = drag_preview
        self.graphboard_view.update_letter(
            self.info_handler.determine_current_letter_and_type()[0]
        )

    def handle_graphboard_view_drag(self, arrow, event):
        '''Dragging an arrow that is already in the graphboard'''
        new_pos = arrow.mapToScene(event.pos()) - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        new_quadrant = arrow.view.get_graphboard_quadrants(new_pos + arrow.center)
        if arrow.quadrant != new_quadrant:
            arrow.quadrant = new_quadrant
            arrow.update_appearance()
            (
                arrow.start_location,
                arrow.end_location,
            ) = arrow.attributes.get_start_end_locations(
                arrow.motion_type, arrow.rotation_direction, arrow.quadrant
            )
            arrow.staff.location = arrow.end_location

            arrow.staff.attributes.update_attributes_from_arrow(arrow)
            arrow.staff.setPos(
                arrow.view.staff_handler.staff_xy_locations[arrow.end_location]
            )
            arrow.view.info_handler.update()
            #delete the old staff

    def handle_pictograph_view_drag(self, arrow, event):
        new_pos = arrow.mapToScene(event.pos()) - arrow.drag_offset / 2
        arrow.setPos(new_pos)

    def select_or_deselect_items(self, event, items):
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if (
                event.button() == Qt.MouseButton.LeftButton
                and event.modifiers() == Qt.KeyboardModifier.ControlModifier
            ):
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.graphboard_view.clear_selection()
                items[0].setSelected(True)

    def set_focus_and_accept_event(self, event):
        self.graphboard_view.setFocus()
        event.accept()

