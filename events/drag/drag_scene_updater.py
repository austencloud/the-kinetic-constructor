from objects.staff.staff import Staff


class DragSceneUpdater:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard_scene = self.drag_manager.graphboard_scene
        self.staff_handler = self.drag_manager.staff_handler
        self.helpers = self.drag_manager.helpers
        
        
    def update_staff(self, drag_preview):
        if not self.drag_manager.event_handler.arrow_dragged:
            return

        for item in self.graphboard_scene.items():
            if isinstance(item, Staff) and item.color == drag_preview.color:
                self.graphboard_scene.removeItem(item)

        staff_dict = self.staff_handler.attributes.create_staff_dict_from_arrow(
            drag_preview
        )
        new_staff = self.helpers.create_and_add_staff(staff_dict)
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

    def cleanup_and_update_scene(self):
        self.event_handler = self.drag_manager.event_handler
        self.event_handler.drag_preview.deleteLater()

        self.drag_manager.staff_handler.update_graphboard_staffs(
            self.drag_manager.graphboard_scene
        )

        self.drag_manager.graphboard_view.update_letter(
            self.drag_manager.info_handler.determine_current_letter_and_type()[0]
        )

        from objects.arrow.arrow import Arrow

        for item in self.drag_manager.graphboard_view.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.arrow_manager.positioner.update_arrow_position(
                    self.drag_manager.graphboard_view
                )

        for item in self.drag_manager.graphboard_view.graphboard_scene.items():
            if isinstance(item, Staff):
                item.setPos(
                    self.drag_manager.graphboard_view.staff_handler.staff_xy_locations[
                        item.location
                    ]
                )

    def update_info_handler(self):
        self.drag_manager.graphboard_view.info_handler.update()
