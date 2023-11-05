from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem
from events.drag.drag_helpers import DragHelpers
from events.drag.drag_scene_updater import DragSceneUpdater
from events.drag.drag_event_handler import DragEventHandler


class DragManager:
    ### INITIALIZATION ###

    def __init__(self):
        self.reset_drag_state()

    def initialize_dependencies(self, graphboard, arrowbox):
        self.arrowbox = arrowbox
        self.graphboard = graphboard
        self.arrow_factory = self.graphboard.main_widget.arrow_manager.factory
        self.info_handler = self.graphboard.info_handler
        self.staff_handler = self.graphboard.staff_handler
        self.staff_factory = self.graphboard.staff_handler.factory
        self.arrow_manager = self.graphboard.main_widget.arrow_manager

        self.helpers = DragHelpers(self)
        self.scene_updater = DragSceneUpdater(self)
        self.event_handler = DragEventHandler(self)

    def reset_drag_state(self):
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

        self.invisible_arrow = None  # Reset the invisible arrow

    ### OBJECT CREATION AND UPDATE ###

    def select_or_deselect_items(self, event, items):
        if items and items[0].flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
            if (
                event.button() == Qt.MouseButton.LeftButton
                and event.modifiers() == Qt.KeyboardModifier.ControlModifier
            ):
                items[0].setSelected(not items[0].isSelected())
            elif not items[0].isSelected():
                self.graphboard.clear_selection()
                items[0].setSelected(True)

    def set_focus_and_accept_event(self, event):
        self.graphboard.setFocus()
        event.accept()
