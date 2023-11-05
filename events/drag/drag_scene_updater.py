from objects.staff.staff import Staff


class DragSceneUpdater:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard = self.drag_manager.graphboard
        self.staff_handler = self.drag_manager.staff_handler
        self.helpers = self.drag_manager.helpers
        self.info_handler = self.drag_manager.info_handler

    def cleanup_and_update_scene(self):
        self.event_handler = self.drag_manager.event_handler
        self.event_handler.drag_preview.deleteLater()
        self.event_handler.drag_preview = None

        self.drag_manager.staff_handler.update_graphboard_staffs(
            self.drag_manager.graphboard
        )

        self.drag_manager.graphboard.update_letter(
            self.drag_manager.info_handler.determine_current_letter_and_type()[0]
        )

        from objects.arrow.arrow import Arrow

        for item in self.drag_manager.graphboard.items():
            if isinstance(item, Arrow):
                item.arrow_manager.positioner.update_arrow_position(
                    self.drag_manager.graphboard
                )

        for item in self.drag_manager.graphboard.items():
            if isinstance(item, Staff) and item.isVisible():
                item.setPos(
                    self.drag_manager.graphboard.staff_handler.staff_xy_locations[
                        item.location
                    ]
                )

    def update_info_handler(self):
        self.drag_manager.graphboard.info_handler.update()
