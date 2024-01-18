from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

from ....attr_box.attr_box_widgets.base_attr_box_widget import AttrBoxWidget

if TYPE_CHECKING:
    from ....attr_box.color_attr_box import ColorAttrBox
    from ....attr_box.lead_state_attr_box import LeadStateAttrBox
    from ....attr_box.motion_type_attr_box import MotionTypeAttrBox


class HeaderWidget(AttrBoxWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "LeadStateAttrBox", "ColorAttrBox", "MotionTypeAttrBox"
        ] = attr_box
        self.setMinimumWidth(self.attr_box.width())
        self.header_label: QLabel = None
        self.separator: QFrame = self.create_separator()

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.header_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.separator)

    def _setup_layout_with_vtg_dir_buttons(self) -> None:
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(5)
        self.layout.addWidget(self.attr_box.rot_dir_button_manager.same_button)
        self.layout.addStretch(1)
        self.layout.addWidget(self.header_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.attr_box.rot_dir_button_manager.opp_button)
        self.layout.addStretch(5)
        self.layout.addWidget(self.separator)

    def _setup_header_label(self, text) -> QLabel:
        font_color = ""
        font_size = 30
        font_weight = "bold"

        if text == "Left":
            font_color = "#2E3192"
        elif text == "Right":
            font_color = "#ED1C24"
        else:
            font_color = "#000000"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )
        return label
