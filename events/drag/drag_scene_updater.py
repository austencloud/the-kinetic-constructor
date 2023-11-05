from objects.staff.staff import Staff


class DragSceneUpdater:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard_view = self.drag_manager.graphboard_view
        self.graphboard_scene = self.drag_manager.graphboard_scene
        self.staff_handler = self.drag_manager.staff_handler
        self.helpers = self.drag_manager.helpers
        self.info_handler = self.drag_manager.info_handler
        


    def cleanup_and_update_scene(self):
        self.event_handler = self.drag_manager.event_handler
        self.event_handler.drag_preview.deleteLater()
        self.event_handler.drag_preview = None

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
            if isinstance(item, Staff) and item.isVisible():
                item.setPos(
                    self.drag_manager.graphboard_view.staff_handler.staff_xy_locations[
                        item.location
                    ]
                )

    def update_info_handler(self):
        self.drag_manager.graphboard_view.info_handler.update()
