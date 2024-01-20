from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

from .attr_box.attr_box_widgets.base_attr_box_widget import AttrBoxWidget

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox

from constants import BLUE, COLOR, LEAD_STATE, MOTION_TYPE, PRO, ANTI, DASH, STATIC


class HeaderWidget(AttrBoxWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: "AttrBox" = attr_box
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header()
        self.layout:QHBoxLayout = self._setup_layout()

    def _setup_header(self) -> None:
        if self.attr_box.attribute_type == COLOR:
            text = "Left" if self.attr_box.color == BLUE else "Right"
            header_label = self._setup_header_label(text)

        elif self.attr_box.attribute_type == LEAD_STATE:
            text = self.attr_box.lead_state.capitalize()
            header_label = self._setup_header_label(text)

        elif self.attr_box.attribute_type == MOTION_TYPE:
            text = self.attr_box.motion_type.capitalize()
            header_label = self._setup_header_label(text)

        return header_label

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.addStretch(5)
        layout.addWidget(self.attr_box.rot_dir_button_manager.same_button)
        layout.addStretch(1)
        layout.addWidget(self.header_label)
        layout.addStretch(1)
        layout.addWidget(self.attr_box.rot_dir_button_manager.opp_button)
        layout.addStretch(5)
        layout.addWidget(self.separator)
        return layout

    def _setup_header_label(self, text: str) -> QLabel:
        font_color = (
            "#000000"
            if text not in ["Left", "Right"]
            else "#2E3192"
            if text == "Left"
            else "#ED1C24"
        )
        font_size = self.attr_box.width() // 4
        font_weight = "bold"
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )
        return label
