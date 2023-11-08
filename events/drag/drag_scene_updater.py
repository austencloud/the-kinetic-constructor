from objects.staff.staff import Staff


class DragSceneUpdater:
    def __init__(self, drag):
        self.drag = drag
        self.graphboard = self.drag.graphboard
        self.helpers = self.drag.helpers

    def cleanup_and_update_scene(self):
        self.events = self.drag.events
        self.events.drag_preview.deleteLater()
        self.events.drag_preview = None
        if self.graphboard.arrows == 2:
            current_letter = self.graphboard.get_current_letter()
            self.graphboard.update_letter(current_letter)
        self.graphboard.update_staffs()
        arrow = self.graphboard.arrows[-1]
        arrow.positioner.update_arrow_position(self.drag.graphboard)
