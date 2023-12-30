from Enums import Direction
from objects.arrow import Arrow
from objects.prop.prop import Prop
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from objects.pictograph.pictograph import Pictograph


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
        sequence = main_widget.sequence_widget

        if not pictograph.selectedItems():
            return
        selection = pictograph.selectedItems()[0]

        selected_arrow = selection if isinstance(selection, Arrow) else None
        selected_prop = selection if isinstance(selection, Prop) else None

        ### DELETION ###
        if event.key() == Qt.Key.Key_Delete:
            keep_prop = event.modifiers() == Qt.KeyboardModifier.ControlModifier
            if selected_arrow:
                selected_arrow.manipulator.delete(keep_prop)
            elif selected_prop:
                selected_prop.manipulator.delete()

        ### ARROW MANIPULATION ###
        if selected_arrow:
            if event.key() == Qt.Key.Key_W:
                selected_arrow.manipulator.move_wasd(Direction.UP)
            elif event.key() == Qt.Key.Key_A:
                selected_arrow.manipulator.move_wasd(Direction.LEFT)
            elif event.key() == Qt.Key.Key_S:
                selected_arrow.manipulator.move_wasd(Direction.DOWN)
            elif event.key() == Qt.Key.Key_D:
                selected_arrow.manipulator.move_wasd(Direction.RIGHT)
            elif event.key() == Qt.Key.Key_R:
                selected_arrow.manipulator.swap_rot_dir()
            elif event.key() == Qt.Key.Key_F:
                selected_arrow.manipulator.swap_motion_type()
            elif event.key() == Qt.Key.Key_Q:
                selected_arrow.motion.subtract_half_turn()
            elif event.key() == Qt.Key.Key_E:
                selected_arrow.motion.add_half_turn()

        ### SEQEUNCE MANAGEMENT ###
        elif event.key() == Qt.Key.Key_Enter:
            pictograph.add_to_sequence_callback()
