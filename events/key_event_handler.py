from objects.arrow.arrow import Arrow
from objects.staff.staff import Staff
from PyQt6.QtCore import Qt


class KeyEventHandler:
    def keyPressEvent(self, event, graphboard):
        main_widget = graphboard.main_widget
        sequence_view = main_widget.sequence_view
        manipulators = graphboard.manipulators
        selected_items = graphboard.selectedItems()
        staff_handler = graphboard.staff_handler
        staff_visibility_manager = staff_handler.visibility_manager

        if len(selected_items) >= 1:
            try:
                selected_item = selected_items[0]
            except IndexError:
                selected_item = None

            selected_arrow_color = None
            if selected_item and isinstance(selected_item, Arrow):
                selected_arrow_color = selected_item.color

            if (
                event.modifiers() == Qt.KeyboardModifier.ControlModifier
                and event.key() == Qt.Key.Key_Delete
            ):
                for item in selected_items:
                    if isinstance(item, Arrow):
                        graphboard.delete_arrow(item, keep_staff=True)
                    elif isinstance(item, Staff):
                        graphboard.delete_staff(item)

            elif event.key() == Qt.Key.Key_Delete:
                for item in selected_items:
                    if isinstance(item, Arrow):
                        graphboard.delete_arrow(item, keep_staff=False)
                        staff_visibility_manager.hide_staff(item.staff)
                    elif isinstance(item, Staff):
                        graphboard.delete_staff(item)

            elif selected_item and isinstance(selected_item, Arrow):
                if event.key() == Qt.Key.Key_W:
                    manipulators.move_arrow_quadrant_wasd("up", selected_item)
                elif event.key() == Qt.Key.Key_A:
                    manipulators.move_arrow_quadrant_wasd("left", selected_item)
                elif event.key() == Qt.Key.Key_S:
                    manipulators.move_arrow_quadrant_wasd("down", selected_item)
                elif event.key() == Qt.Key.Key_D:
                    manipulators.move_arrow_quadrant_wasd("right", selected_item)
                elif event.key() == Qt.Key.Key_R:
                    manipulators.mirror_arrow(selected_items, selected_arrow_color)
                elif event.key() == Qt.Key.Key_F:
                    manipulators.swap_motion_type(
                        selected_items, selected_arrow_color
                    )
                elif event.key() == Qt.Key.Key_Enter:
                    sequence_view.add_to_sequence(graphboard)
                elif event.key() == Qt.Key.Key_Q:
                    manipulators.decrement_turns(
                        selected_items, selected_arrow_color
                    )
                elif event.key() == Qt.Key.Key_E:
                    manipulators.increment_turns(
                        selected_items, selected_arrow_color
                    )
