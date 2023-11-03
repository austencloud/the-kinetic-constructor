from events.drag.drag_preview import DragPreview


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
        self.staff_factory = self.staff_handler.factory

    ### DRAG INIT ###

    def start_drag(self, view, target_arrow, event):
        if not self.helpers.is_click_on_arrow(view, event):
            return
        self.setup_drag_preview(view, target_arrow, event)

    def setup_drag_preview(self, view, target_arrow, event):
        self.drag_preview = DragPreview(self.drag_manager, target_arrow)
        self.arrow_dragged = True
        self.dragging = True
        self.target_arrow = target_arrow
        self.graphboard_view.dragged_arrow = self.target_arrow
        self.drag_preview.setParent(view.main_widget)
        self.drag_preview.show()
        self.drag_preview.move_to_cursor(view, event, self.target_arrow)

    ### DRAG INTO GRAPHBOARD ###

    def handle_drag_into_graphboard(self, view, event):
        if self.drag_preview:
            self.update_drag_preview_for_graphboard(view, event)

    def update_drag_preview_for_graphboard(self, view, event):
        if not self.drag_preview.has_entered_graphboard_once:
            self.just_entered_graphboard = True
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
        new_arrow_dict = self.target_arrow.attributes.create_dict_from_arrow(
            self.drag_preview
        )
        self.invisible_arrow = self.helpers.create_and_add_arrow(new_arrow_dict)
        self.invisible_arrow.setVisible(False)

        self.new_staff_dict = self.staff_attributes.create_staff_dict_from_arrow(
            self.drag_preview
        )


        for staff in self.graphboard_view.staffs:
            if staff.color == self.drag_preview.color:
                staff.attributes.update_attributes_from_dict(staff, self.new_staff_dict)
                staff.arrow = self.invisible_arrow
                self.invisible_arrow.staff = staff
                staff.location = staff.arrow.end_location
                staff.update_appearance()
                staff.setVisible(True)   
        
        self.staff_handler.update_graphboard_staffs(self.graphboard_scene)

        self.invisible_arrow.arrow_manager.attributes.update_attributes(
            self.invisible_arrow, new_arrow_dict
        )

        self.info_handler.update()

    ### MOUSE MOVE ###

    def handle_mouse_move(self, view, event):
        if self.drag_preview:
            self.update_drag_preview_on_mouse_move(view, event)

    def update_drag_preview_on_mouse_move(self, view, event):
        self.update_arrow_drag_preview(view, event)

        if self.drag_preview.has_entered_graphboard_once:
            new_arrow_dict = self.arrow_manager.attributes.create_dict_from_arrow(
                self.drag_preview
            )
            self.invisible_arrow.arrow_manager.attributes.update_attributes(
                self.invisible_arrow, new_arrow_dict
            )  # Implement a method to update arrow's properties
            board_state = self.graphboard_view.get_state()
            self.staff_handler.positioner.reposition_staffs(
                self.graphboard_scene, board_state
            )
            self.info_handler.update()

    def update_arrow_drag_preview(self, view, event):
        """Update the arrow's drag preview."""
        over_graphboard = self.helpers.is_over_graphboard(view, event)

        if over_graphboard:
            self.handle_drag_into_graphboard(view, event)

        self.drag_preview.move_to_cursor(view, event, self.target_arrow)

    ### MOUSE RELEASE ###

    def handle_mouse_release(self, event):
        if self.drag_preview:
            self.handle_drop_event(event)
            self.drag_manager.reset_drag_state()

    def handle_drop_event(self, event):
        if self.dragging:
            self.place_arrow_on_graphboard(event)
            self.scene_updater.cleanup_and_update_scene()
            self.scene_updater.update_info_handler()

    def place_arrow_on_graphboard(self, event):
        placed_arrow = self.invisible_arrow
        placed_arrow.setVisible(True)

        if self.drag_preview.has_entered_graphboard_once:
            self.drag_manager.set_focus_and_accept_event(event)

            self.graphboard_view.clear_selection()
            placed_arrow.setSelected(True)

    ### MOUSE PRESS EVENTS ###

    def handle_mouse_press(self, event):
        self.graphboard_view.setFocus()
        items = self.graphboard_view.items(event.pos())
        self.drag_manager.select_or_deselect_items(event, items)
        if not items or not items[0].isSelected():
            self.graphboard_view.clear_selection()
