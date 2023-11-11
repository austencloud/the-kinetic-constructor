from objects.arrow import Arrow
from objects.staff import Staff
from PyQt6.QtCore import Qt
from settings.string_constants import *


class KeyEventHandler:
    def keyPressEvent(self, event, main_widget, graphboard):
        sequence_view = main_widget.sequence_view
        
        if not graphboard.selectedItems():
            return
        selection = graphboard.selectedItems()[0]

        selected_arrow = selection if isinstance(selection, Arrow) else None
        selected_staff = selection if isinstance(selection, Staff) else None

        ### DELETION ###
        if event.key() == Qt.Key.Key_Delete:
            keep_staff = event.modifiers() == Qt.KeyboardModifier.ControlModifier
            if selected_arrow:
                graphboard.delete_arrow(selected_arrow, keep_staff=keep_staff)
            elif selected_staff:
                graphboard.delete_staff(selected_staff)

        ### ARROW MANIPULATION ###
        if event.key() == Qt.Key.Key_W:
            selected_arrow.move_wasd(UP)
        elif event.key() == Qt.Key.Key_A:
            selected_arrow.move_wasd(LEFT)
        elif event.key() == Qt.Key.Key_S:
            selected_arrow.move_wasd(DOWN)
        elif event.key() == Qt.Key.Key_D:
            selected_arrow.move_wasd(RIGHT)
        elif event.key() == Qt.Key.Key_R:
            selected_arrow.mirror_arrow()
        elif event.key() == Qt.Key.Key_F:
            selected_arrow.swap_motion_type()
        elif event.key() == Qt.Key.Key_Q:
            selected_arrow.decrement_turns()
        elif event.key() == Qt.Key.Key_E:
            selected_arrow.increment_turns()

        ### SEQEUNCE MANAGEMENT ###
        elif event.key() == Qt.Key.Key_Enter:
            sequence_view.add_to_sequence(graphboard)
