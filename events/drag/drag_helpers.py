

class DragHelpers:
    def __init__(self, drag):
        self.drag = drag
        self.graphboard = self.drag.graphboard

    def is_over_graphboard(self, scene, event_pos):
        pos_in_main_window = scene.view.mapTo(scene.main_widget, event_pos)
        local_pos_in_graphboard = self.drag.graphboard.view.mapFrom(
            scene.main_widget, pos_in_main_window
        )
        return self.drag.graphboard.view.rect().contains(local_pos_in_graphboard)

    def get_local_pos_in_graphboard(self, scene, event_pos):
        return self.drag.graphboard.view.mapFrom(
            scene.main_widget, scene.view.mapTo(scene.main_widget, event_pos)
        )



    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow
