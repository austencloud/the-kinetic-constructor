from PyQt6.QtWidgets import QGraphicsItem


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

    def create_and_add_arrow(self, arrow_dict):
        from objects.arrow.arrow import Arrow

        arrow = Arrow(self.graphboard, arrow_dict)
        arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard.addItem(arrow)
        if arrow not in self.graphboard.arrows:
            self.graphboard.arrows.append(arrow)
        return arrow

    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow
