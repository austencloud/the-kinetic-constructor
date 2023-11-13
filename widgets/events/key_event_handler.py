from objects.arrow import Arrow
from objects.staff import Staff
from PyQt6.QtCore import Qt
from settings.string_constants import *


class KeyEventHandler:
    def keyPressEvent(self, event, main_widget, graphboard):
        sequence_scene = main_widget.sequence_scene

        if not graphboard.selectedItems():
            return
        selection = graphboard.selectedItems()[0]

        selected_arrow = selection if isinstance(selection, Arrow) else None
        selected_staff = selection if isinstance(selection, Staff) else None

        ### DELETION ###
        if event.key() == Qt.Key.Key_Delete:
            keep_staff = event.modifiers() == Qt.KeyboardModifier.ControlModifier
            if selected_arrow:
                selected_arrow.delete(keep_staff)
            elif selected_staff:
                selected_staff.delete()

        ### ARROW MANIPULATION ###

        if selected_arrow:
            if event.key() == Qt.Key.Key_W:
                selected_arrow.move_wasd(UP)
            elif event.key() == Qt.Key.Key_A:
                selected_arrow.move_wasd(LEFT)
            elif event.key() == Qt.Key.Key_S:
                selected_arrow.move_wasd(DOWN)
            elif event.key() == Qt.Key.Key_D:
                selected_arrow.move_wasd(RIGHT)
            elif event.key() == Qt.Key.Key_R:
                selected_arrow.mirror()
            elif event.key() == Qt.Key.Key_F:
                selected_arrow.swap_motion_type()
            elif event.key() == Qt.Key.Key_Q:
                selected_arrow.decrement_turns()
            elif event.key() == Qt.Key.Key_E:
                selected_arrow.increment_turns()

        ### SEQEUNCE MANAGEMENT ###
        elif event.key() == Qt.Key.Key_Enter:
            sequence_scene.add_to_sequence(graphboard)
