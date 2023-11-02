from events.drag.drag_preview import DragPreview
from PyQt5.QtWidgets import QApplication

class DragEventHandler:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.helpers = self.drag_manager.helpers
        self.graphboard_view = self.drag_manager.graphboard_view
    ### DRAG EVENT HANDLING ###

    def start_drag(self, view, arrow, event):
        if not self.helpers.is_click_on_arrow(view, event):
            return
        self.drag_preview = DragPreview(self, arrow)
        self.arrow_dragged = True  # Set the flag
        self.dragging = True
        self.arrow = arrow
        self.graphboard_view.dragged_arrow = self.arrow
        self.drag_preview = DragPreview(self, arrow)
        self.drag_preview.setParent(QApplication.instance().activeWindow())
        self.drag_preview.show()
        self.drag_preview.move_to_cursor(view, event, self.arrow)

    def handle_mouse_press(self, event):
        self.graphboard_view.setFocus()
        items = self.graphboard_view.items(event.pos())
        self.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard_view.clear_selection()

    def handle_mouse_move(self, view, event):
        if self.drag_preview is not None:
            self.update_arrow_drag_preview(view, event)
            self.graphboard_view.dragMoveEvent(event, self.drag_preview)

            if self.has_entered_graphboard_once:
                new_arrow_dict = self.arrow.attributes.create_dict_from_arrow(self.drag_preview)
                self.invisible_arrow.arrow_manager.arrow_attributes.update_attributes(
                    self.invisible_arrow, new_arrow_dict
                )  # Implement a method to update arrow's properties
                board_state = self.graphboard_view.get_state()
                self.staff_handler.staff_positioner.reposition_staffs(
                    self.graphboard_scene, board_state
                )
                self.info_handler.update()

    def handle_drag_into_graphboard(self, view, event):
        """Dragging an arrow from the arrowbox into the graphboard"""
        if not self.drag_preview:
            return

        if not self.has_entered_graphboard_once:
            self.has_entered_graphboard_once = True

        local_pos_in_graphboard = self.get_local_pos_in_graphboard(view, event)
        new_quadrant = self.graphboard_view.get_graphboard_quadrants(
            self.graphboard_view.mapToScene(local_pos_in_graphboard)
        )

        from objects.arrow.arrow import Arrow

        for arrow in self.graphboard_scene.items():
            if isinstance(arrow, Arrow) and arrow.color == self.arrow.color:
                self.graphboard_scene.removeItem(arrow)

        self.drag_preview.update_rotation_for_quadrant(new_quadrant)
        new_arrow_dict = self.create_arrow_dict_from_drag_preview()
        self.invisible_arrow = self.create_and_add_arrow(new_arrow_dict)
        self.update_staff(self.drag_preview)
        self.invisible_arrow.staff = self.staff
        self.staff.arrow = self.invisible_arrow
        self.invisible_arrow.setVisible(False)

        # Update the invisible arrow's attributes
        self.invisible_arrow.arrow_manager.arrow_attributes.update_attributes(
            self.invisible_arrow, new_arrow_dict
        )

        # Update staffs and letter
        self.update_staff(self.drag_preview)
        self.info_handler.update()

    def handle_mouse_release(self, view, event, drag_preview):
        if not hasattr(self, "drag_preview"):
            return

        self.handle_drop_event(event)
        self.reset_drag_state()

    def handle_drop_event(self, event):
        if not self.dragging:
            return

        self.invisible_arrow.deleteLater()

        if self.has_entered_graphboard_once:
            self.set_focus_and_accept_event(event)
            new_arrow_dict = self.create_arrow_dict_from_drag_preview()
            new_staff_dict = self.create_staff_dict_from_drag_preview()

            # Make the invisible arrow visible
            self.invisible_arrow.setVisible(True)

            new_arrow = self.create_and_add_arrow(new_arrow_dict)
            new_staff = self.create_and_add_staff(new_staff_dict)

            self.graphboard_view.clear_selection()
            new_arrow.setSelected(True)

            self.link_arrow_and_staff(new_arrow, new_staff)

        self.cleanup_and_update_scene()
        self.update_info_handler()
