from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Callable, Union

from constants import ICON_DIR
from objects.motion.motion import Motion
from .attr_box_button import AdjustTurnsButton

if TYPE_CHECKING:
    pass


class BaseAttrBoxWidget(QWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box

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

    def create_attr_box_button(
        self, icon_path: str, callback: Callable
    ) -> AdjustTurnsButton:
        button = AdjustTurnsButton(self)
        button.setIcon(QIcon(ICON_DIR + icon_path))
        button.clicked.connect(callback)
        return button

    def _turns_added(self, initial_turns, new_turns) -> bool:
        return initial_turns == 0 and new_turns > 0

    def update_pictograph_dict(
        self, motion: Motion, new_turns: Union[int, float]
    ) -> None:
        """Update the pictograph dictionary with new turns."""
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def get_vtg_dir_btn_style(self, pressed: bool) -> str:
        if pressed:
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                    padding: 5px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """
