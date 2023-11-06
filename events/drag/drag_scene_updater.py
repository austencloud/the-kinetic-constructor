from objects.staff.staff import Staff


class DragSceneUpdater:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard = self.drag_manager.graphboard
        self.helpers = self.drag_manager.helpers

    def cleanup_and_update_scene(self):
        self.event_handler = self.drag_manager.event_handler
        self.event_handler.drag_preview.deleteLater()
        self.event_handler.drag_preview = None

        current_letter = self.graphboard.determine_current_letter_and_type()[0]
        self.graphboard.update_staffs()
        self.graphboard.update_letter(current_letter)

        from objects.arrow.arrow import Arrow

        for item in self.drag_manager.graphboard.items():
            if isinstance(item, Arrow):
                item.positioner.update_arrow_position(
                    self.drag_manager.graphboard
                )

