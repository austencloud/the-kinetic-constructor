from PyQt6.QtWidgets import QGraphicsItem


class DragHelpers:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
        self.graphboard = self.drag_manager.graphboard
        self.staff_handler = self.drag_manager.staff_handler
        self.staff_factory = self.drag_manager.staff_factory
        self.arrow_factory = self.drag_manager.arrow_factory

    def is_over_graphboard(self, scene, event_pos):
        pos_in_main_window = scene.view.mapTo(scene.main_widget, event_pos)
        local_pos_in_graphboard = self.drag_manager.graphboard.view.mapFrom(
            scene.main_widget, pos_in_main_window
        )
        return self.drag_manager.graphboard.view.rect().contains(
            local_pos_in_graphboard
        )

    def get_local_pos_in_graphboard(self, scene, event_pos):
        return self.drag_manager.graphboard.view.mapFrom(
            scene.main_widget, scene.view.mapTo(scene.main_widget, event_pos)
        )

    def create_and_add_arrow(self, arrow_dict):
        new_arrow = self.arrow_factory.create_arrow(self.graphboard, arrow_dict)
        new_arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.graphboard.addItem(new_arrow)
        return new_arrow

    def link_arrow_and_staff(self, arrow, staff):
        arrow.staff = staff
        staff.arrow = arrow
