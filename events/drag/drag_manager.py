from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem, QApplication
from PyQt6.QtGui import QCursor, QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from resources.constants import GRAPHBOARD_SCALE, STATIC
from events.drag.drag_preview import DragPreview
from objects.staff.staff import Staff
from events.drag.drag_helpers import DragHelpers
from events.drag.drag_scene_updater import DragSceneUpdater
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
            self.graphboard_view.main_widget.arrow_manager.factory
        )
        self.info_handler = self.graphboard_view.info_handler
        self.staff_handler = self.graphboard_view.staff_handler
        self.staff_factory = self.graphboard_view.staff_handler.factory
        self.arrow_manager = self.graphboard_view.main_widget.arrow_manager
        
        self.helpers = DragHelpers(self)
        self.scene_updater = DragSceneUpdater(self)
        self.event_handler = DragEventHandler(self)
        

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

        self.invisible_arrow = None  # Reset the invisible arrow

    ### OBJECT CREATION AND UPDATE ###

    def handle_graphboard_view_drag(self, arrow, event):
        """Dragging an arrow that is already in the graphboard"""
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
            # delete the old staff

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
