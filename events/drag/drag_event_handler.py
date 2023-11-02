from events.drag.drag_preview import DragPreview
from PyQt5.QtWidgets import QApplication

class DragEventHandler:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.helpers = self.drag_manager.helpers
        self.graphboard_view = self.drag_manager.graphboard_view
        self.graphboard_scene = self.drag_manager.graphboard_scene
        self.scene_updater = self.drag_manager.scene_updater
        self.info_handler = self.drag_manager.info_handler
        self.staff_handler = self.drag_manager.staff_handler
        self.arrow_manager = self.drag_manager.arrow_manager
        self.arrow_attributes = self.arrow_manager.attributes
        self.staff_attributes = self.staff_handler.attributes

    def start_drag(self, view, target_arrow, event):
        if not self.helpers.is_click_on_arrow(view, event):
            return
        self.drag_preview = DragPreview(self.drag_manager, target_arrow)
        self.arrow_dragged = True  # Set the flag
        self.dragging = True
        self.target_arrow = target_arrow
        self.graphboard_view.dragged_arrow = self.target_arrow
        self.drag_preview.setParent(view.main_widget)
        self.drag_preview.show()
        self.drag_preview.move_to_cursor(view, event, self.target_arrow)

    def handle_mouse_press(self, event):
        self.graphboard_view.setFocus()
        items = self.graphboard_view.items(event.pos())
        self.drag_manager.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard_view.clear_selection()

    def handle_mouse_move(self, view, event):
        if self.drag_preview is not None:
            self.helpers.update_arrow_drag_preview(view, event)
            self.graphboard_view.dragMoveEvent(event, self.drag_preview)

            if self.drag_preview.has_entered_graphboard_once:
                new_arrow_dict = view.arrow_manager.attributes.create_dict_from_arrow(self.drag_preview)
                self.invisible_arrow.arrow_manager.attributes.update_attributes(
                    self.invisible_arrow, new_arrow_dict
                )  # Implement a method to update arrow's properties
                board_state = self.graphboard_view.get_state()
                self.staff_handler.positioner.reposition_staffs(
                    self.graphboard_scene, board_state
                )
                self.info_handler.update()

    def handle_drag_into_graphboard(self, view, event):
        """Dragging an arrow from the arrowbox into the graphboard"""
        if not self.drag_preview:
            return

        if not self.drag_preview.has_entered_graphboard_once:
            self.drag_preview.has_entered_graphboard_once = True

        local_pos_in_graphboard = self.helpers.get_local_pos_in_graphboard(view, event)
        new_quadrant = self.graphboard_view.get_graphboard_quadrants(
            self.graphboard_view.mapToScene(local_pos_in_graphboard)
        )

        from objects.arrow.arrow import Arrow

        for item in self.drag_manager.graphboard_scene.items():
            if isinstance(item, Arrow) and item.color == self.drag_preview.color:
                self.graphboard_scene.removeItem(item)

        self.drag_preview.update_rotation_for_quadrant(new_quadrant)
        new_arrow_dict = self.target_arrow.attributes.create_dict_from_arrow(self.drag_preview)
        self.invisible_arrow = self.helpers.create_and_add_arrow(new_arrow_dict)
        self.drag_manager.scene_updater.update_staff(self.drag_preview)
        self.invisible_arrow.staff = self.scene_updater.staff
        self.scene_updater.staff.arrow = self.invisible_arrow
        self.invisible_arrow.setVisible(False)

        # Update the invisible arrow's attributes
        self.invisible_arrow.arrow_manager.attributes.update_attributes(
            self.invisible_arrow, new_arrow_dict
        )

        # Update staffs and letter
        self.scene_updater.update_staff(self.drag_preview)
        self.info_handler.update()

    def handle_mouse_release(self, view, event, drag_preview):
        if not hasattr(self, "drag_preview"):
            return

        self.handle_drop_event(event)
        self.drag_manager.reset_drag_state()

    def handle_drop_event(self, event):
        if not self.dragging:
            return

        self.invisible_arrow.deleteLater()

        if self.drag_preview.has_entered_graphboard_once:
            self.drag_manager.set_focus_and_accept_event(event)
            new_arrow_dict = self.arrow_attributes.create_dict_from_arrow(self.drag_preview)
            new_staff_dict = self.staff_attributes.create_staff_dict_from_arrow(self.drag_preview)

            # Make the invisible arrow visible
            self.invisible_arrow.setVisible(True)

            new_arrow = self.helpers.create_and_add_arrow(new_arrow_dict)
            new_staff = self.helpers.create_and_add_staff(new_staff_dict)

            self.graphboard_view.clear_selection()
            new_arrow.setSelected(True)

            self.helpers.link_arrow_and_staff(new_arrow, new_staff)

        self.scene_updater.cleanup_and_update_scene()
        self.scene_updater.update_info_handler()
