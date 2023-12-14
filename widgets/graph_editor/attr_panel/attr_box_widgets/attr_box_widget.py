from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Callable

from constants.string_constants import ICON_DIR
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class AttrBoxWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
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

    def create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_custom_button(self, icon_path: str, callback: Callable) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(ICON_DIR + icon_path))
        button.clicked.connect(callback)
        return button

