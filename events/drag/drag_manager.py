from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem
from events.drag.drag_helpers import DragHelpers
from events.drag.drag_scene_updater import DragSceneUpdater
from events.drag.drag_events import DragEvents


class DragManager:
    ### INITIALIZATION ###

    def __init__(self, main_window):
        self.main_window = main_window
        self.reset_drag_state()

    def initialize_dependencies(self, main_window, graphboard, arrowbox):
        self.arrowbox = arrowbox
        self.graphboard = graphboard
        self.main_window = main_window
        self.helpers = DragHelpers(self)
        self.scene_updater = DragSceneUpdater(self)
        self.event_handler = DragEvents(self)

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
