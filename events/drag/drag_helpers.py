from events.drag.drag_preview import DragPreview


class DragHelpers:
    def __init__(self, drag_manager):
        self.drag_manager = drag_manager
    

    @staticmethod
    def is_click_on_arrow(view, event):
        from objects.arrow.arrow import Arrow

        items = view.items(event.pos())
        return any(isinstance(item, Arrow) for item in items)

    @staticmethod
    def update_arrow_drag_preview(drag_manager, view, event):
        over_graphboard = DragHelpers.is_over_graphboard(drag_manager, view, event)

        if over_graphboard:
            drag_manager.handle_drag_into_graphboard(view, event)

        drag_manager.drag_preview.move_to_cursor(view, event, drag_manager.arrow)

    @staticmethod
    def is_over_graphboard(drag_manager, view, event):
        pos_in_main_window = view.mapTo(view.window(), event.pos())
        local_pos_in_graphboard = drag_manager.graphboard_view.mapFrom(
            view.window(), pos_in_main_window
        )
        return drag_manager.graphboard_view.rect().contains(local_pos_in_graphboard)

    @staticmethod
    def get_local_pos_in_graphboard(drag_manager, view, event):
        return drag_manager.graphboard_view.mapFrom(
            view.window(), view.mapTo(view.window(), event.pos())
        )
