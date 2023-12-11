from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox
from PyQt6.QtGui import QFont, QIcon, QResizeEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional, Callable

from settings.string_constants import ICON_DIR, SWAP_ICON
from widgets.graph_editor.attr_panel.custom_button import CustomButton
from utilities.TypeChecking.TypeChecking import MotionTypes, Locations

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class AttrBoxWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box

    def create_label(
        self,
        text: str,
        font_size: int,
        align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
    ) -> QLabel:
        label = QLabel(text, self)
        label.setFont(QFont("Arial", font_size))
        label.setAlignment(align)
        return label

    def create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_custom_button(self, icon_path: str, callback: Callable) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(ICON_DIR + icon_path))
        button.clicked.connect(callback)
        return button

    def setup_header_label_frame(
        self, text: str, frame_layout: QHBoxLayout | QVBoxLayout
    ) -> QFrame:
        label = self.create_label(text, int(self.attr_box.attr_panel.width() / 35))
        frame = self.create_frame(frame_layout)
        frame_layout.addWidget(label)
        return frame

    def resize_event_logic(self, event: QResizeEvent, components: list) -> None:
        super().resizeEvent(event)
        common_height = max(component.sizeHint().height() for component in components)
        for component in components:
            component.setMaximumHeight(common_height)

