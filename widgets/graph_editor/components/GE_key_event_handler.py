from data.constants import DOWN, LEFT, RIGHT, UP
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.pictograph.pictograph import Pictograph


class GE_KeyEventHandler:
    def keyPressEvent(
        self, event: "QKeyEvent", main_widget: "MainWidget", pictograph: "Pictograph"
    ) -> None:

        if not pictograph.selectedItems():
            return
        selection = pictograph.selectedItems()[0]

        selected_arrow = selection if isinstance(selection, Arrow) else None
        selected_motion = selected_arrow.motion
        if selected_arrow:
            key_actions = {
                Qt.Key.Key_W: selected_motion.manipulator.move_wasd(UP),
                Qt.Key.Key_A: selected_motion.manipulator.move_wasd(LEFT),
                Qt.Key.Key_S: selected_motion.manipulator.move_wasd(DOWN),
                Qt.Key.Key_D: selected_motion.manipulator.move_wasd(RIGHT),
                Qt.Key.Key_R: selected_motion.manipulator.swap_rot_dir(),
                Qt.Key.Key_F: selected_motion.manipulator.swap_motion_type()
            }
            if event.key() in key_actions:
                key_actions[event.key()]


