from objects.arrow.arrow import Arrow
from objects.staff.staff import Staff
from PyQt6.QtCore import Qt
from settings.string_constants import *
class KeyEventHandler:
    def keyPressEvent(self, event, main_widget, graphboard, manipulators):
        sequence_view = main_widget.sequence_view
        selection = graphboard.selectedItems()

        if len(selection) >= 1:
            try:
                selected_item = selection[0]
            except IndexError:
                selected_item = None

            selected_arrow_color = None
            if selected_item and isinstance(selected_item, Arrow):
                selected_arrow_color = selected_item.color

            # Handle deletion with Ctrl+Delete or just Delete
            if event.key() == Qt.Key.Key_Delete:
                keep_staff = event.modifiers() == Qt.KeyboardModifier.ControlModifier
                for item in selection:
                    if isinstance(item, Arrow):
                        graphboard.delete_arrow(item, keep_staff=keep_staff)
                        if not keep_staff:
                            graphboard.delete_staff(item.staff)
                    elif isinstance(item, Staff):
                        graphboard.delete_staff(item)

            # Handle arrow-specific actions
            if selected_item and isinstance(selected_item, Arrow):
                if event.key() == Qt.Key.Key_W:
                    manipulators.move_wasd(UP, selected_item)
                elif event.key() == Qt.Key.Key_A:
                    manipulators.move_wasd(LEFT, selected_item)
                elif event.key() == Qt.Key.Key_S:
                    manipulators.move_wasd(DOWN, selected_item)
                elif event.key() == Qt.Key.Key_D:
                    manipulators.move_wasd(RIGHT, selected_item)
                elif event.key() == Qt.Key.Key_R:
                    manipulators.mirror_arrow(selected_item)
                elif event.key() == Qt.Key.Key_F:
                    manipulators.swap_motion_type(selected_item)
                elif event.key() == Qt.Key.Key_Enter:
                    sequence_view.add_to_sequence(graphboard)
                elif event.key() == Qt.Key.Key_Q:
                    selected_item.decrement_turns()
                elif event.key() == Qt.Key.Key_E:
                    selected_item.increment_turns()
