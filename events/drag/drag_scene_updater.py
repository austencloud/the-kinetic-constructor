from objects.staff.staff import Staff

class SceneUpdater:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager

    def cleanup_and_update_scene(self):
        self.drag_manager.drag_preview.deleteLater()

        self.drag_manager.staff_handler.update_graphboard_staffs(
            self.drag_manager.graphboard_scene
        )

        self.drag_manager.graphboard_view.update_letter(
            self.drag_manager.info_handler.determine_current_letter_and_type()[0]
        )

        from objects.arrow.arrow import Arrow

        for item in self.drag_manager.graphboard_view.graphboard_scene.items():
            if isinstance(item, Arrow):
                item.arrow_manager.arrow_positioner.update_arrow_position(
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
