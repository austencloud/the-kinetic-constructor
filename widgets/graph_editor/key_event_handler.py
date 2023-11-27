from objects.arrow import Arrow
from objects.props.staff import Staff
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from settings.string_constants import UP, LEFT, DOWN, RIGHT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class KeyEventHandler:
    """
    Handles key events for the graph editor.

    Args:
        event (QKeyEvent): The key event.
        main_widget (MainWidget): The main widget.
        pictograph (Pictograph): The graph board.

    Returns:
        None
    """

    def keyPressEvent(
        self, event: "QKeyEvent", main_widget: "MainWidget", pictograph: "Pictograph"
    ) -> None:
        """
        Handles the key press event.

        Args:
            event (QKeyEvent): The key event.
            main_widget (MainWidget): The main widget.
            pictograph (Pictograph): The graph board.

        Returns:
            None
        """
        sequence = main_widget.sequence

        if not pictograph.selectedItems():
            return
        selection = pictograph.selectedItems()[0]

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
                selected_arrow.swap_rot_dir()
            elif event.key() == Qt.Key.Key_F:
                selected_arrow.swap_motion_type()
            elif event.key() == Qt.Key.Key_Q:
                selected_arrow.motion.subtract_half_turn()
            elif event.key() == Qt.Key.Key_E:
                selected_arrow.motion.add_half_turn()

        ### SEQEUNCE MANAGEMENT ###
        elif event.key() == Qt.Key.Key_Enter:
            sequence.add_to_sequence(pictograph)
