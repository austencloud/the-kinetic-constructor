from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Callable, Union

from widgets.buttons.swap_button import SwapButton

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion
from ...buttons.adjust_turns_button import AdjustTurnsButton

if TYPE_CHECKING:
    pass


class AttrBoxWidget(QWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: "AttrBox" = attr_box

    def create_attr_header_label(
        self, text: str, align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ) -> QLabel:
        attr_label = QLabel(text, self)
        attr_label.setFont(QFont("Arial", self.attr_box.font_size))
        attr_label.setAlignment(align)
        attr_label.setContentsMargins(0, 0, 0, 0)
        return attr_label

    def create_header_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_swap_button(self, icon_path: str, callback: Callable) -> "SwapButton":
        button = SwapButton(self.attr_box, icon_path)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def create_adjust_turns_button(self, text: str) -> AdjustTurnsButton:
        button = AdjustTurnsButton(self)
        button.setText(text)
        return button

    def _turns_added(self, initial_turns, new_turns) -> bool:
        return initial_turns == 0 and new_turns > 0

    def update_pictograph_dict(
        self, motion: "Motion", new_turns: Union[int, float]
    ) -> None:
        """Update the pictograph dictionary with new turns."""
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.pictograph.state_updater.update_pictograph(pictograph_dict)
