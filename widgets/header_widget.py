from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

from Enums.Enums import LetterType, TurnsTabAttribute
from Enums.MotionAttributes import Colors


from .turns_box.turns_box_widgets.base_attr_box_widget import TurnsBoxWidget

if TYPE_CHECKING:
    from widgets.turns_box.turns_box import TurnsBox



class TurnsBoxHeaderWidget(TurnsBoxWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header()
        self.layout: QHBoxLayout = self._setup_layout()

    def _setup_header(self) -> None:
        if self.turns_box.attribute_type == TurnsTabAttribute.COLOR:
            if self.turns_box.color == Colors.BLUE:
                text = "Left"
            elif self.turns_box.color == Colors.RED:
                text = "Right"
            header_label = self._setup_header_label(text)

        elif self.turns_box.attribute_type == TurnsTabAttribute.LEAD_STATE:
            text = self.turns_box.lead_state.value.capitalize()
            header_label = self._setup_header_label(text)

        elif self.turns_box.attribute_type == TurnsTabAttribute.MOTION_TYPE:
            text = self.turns_box.motion_type.value.capitalize()
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._add_widgets(layout)
        return layout

    def _add_widgets(self, layout: QHBoxLayout) -> None:
        if self.turns_box.turns_panel.turns_tab.section.letter_type == LetterType.Type1:
            layout.addStretch(1)
            layout.addWidget(self.header_label)
            layout.addStretch(1)
        else:
            layout.addStretch(5)
            layout.addWidget(self.turns_box.prop_rot_dir_button_manager.ccw_button)
            layout.addStretch(1)
            layout.addWidget(self.header_label)
            layout.addStretch(1)
            layout.addWidget(self.turns_box.prop_rot_dir_button_manager.cw_button)
            layout.addStretch(5)
            layout.addWidget(self.separator)

    def _setup_header_label(self, text: str) -> QLabel:
        font_color = (
            "#000000"
            if text not in ["Left", "Right"]
            else "#2E3192" if text == "Left" else "#ED1C24"
        )
        font_size = self.turns_box.width() // 4
        font_weight = "bold"
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )
        label.setMaximumHeight(font_size * 2)
        self.adjustSize()
        return label
