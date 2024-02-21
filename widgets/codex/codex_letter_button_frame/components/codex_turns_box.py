from typing import TYPE_CHECKING, cast
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from Enums.Enums import TurnsTabAttribute
from Enums.MotionAttributes import Color, LeadStates, MotionType

from constants import BLUE, CLOCKWISE, COLOR, COUNTER_CLOCKWISE, RED
from widgets.codex.codex_letter_button_frame.components.codex_turns_box_header_widget import (
    CodexTurnsBoxHeader,
)

from .codex_prop_rot_dir_button_manager import (
    CodexPropRotDirButtonManager,
)
from ...codex_turns_widget import (
    CodexTurnsWidget,
)

if TYPE_CHECKING:
    from widgets.codex_turns_panel import CodexTurnsPanel


class CodexTurnsBox(QFrame):
    turns_widget: CodexTurnsWidget

    def __init__(
        self,
        turns_panel,
        attribute_type: TurnsTabAttribute,
        attribute: TurnsTabAttribute,
    ) -> None:
        super().__init__(turns_panel)
        self.attribute_type: TurnsTabAttribute = attribute_type
        self.attribute_value = attribute
        self.turns_panel: "CodexTurnsPanel" = turns_panel

        self.font_size = self.turns_panel.width() // 20
        self.turn_display_border = 2
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }

        self.motion_type: TurnsTabAttribute
        self.color: TurnsTabAttribute
        self.lead_state: TurnsTabAttribute

        self._setup_attribute_type()
        self._setup_widgets()
        self._setup_layouts()

    def _setup_attribute_type(self) -> None:
        if self.attribute_type == TurnsTabAttribute.MOTION_TYPE:
            self.motion_type = cast(MotionType, self.attribute_value)
        elif self.attribute_type == TurnsTabAttribute.COLOR:
            self.color = cast(Color, self.attribute_value)
        elif self.attribute_type == TurnsTabAttribute.LEAD_STATE:
            self.lead_state = cast(LeadStates, self.attribute_value)

    def _setup_widgets(self) -> None:
        self.prop_rot_dir_button_manager = CodexPropRotDirButtonManager(self)
        self.header_widget = CodexTurnsBoxHeader(self)
        self.turns_widget = CodexTurnsWidget(self)

        if self.attribute_type == COLOR:
            if self.color == RED:
                self.apply_border_style("#ED1C24")
            elif self.color == BLUE:
                self.apply_border_style("#2E3192")
        else:
            self.apply_border_style("#000000")  # Black border

    def _setup_layouts(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.header_widget.separator)
        self.layout.addWidget(self.turns_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def apply_border_style(self, color_hex: str) -> None:
        border_width = 1 if color_hex == "#000000" else 2
        self.setStyleSheet(
            f"#TurnsBox {{ "
            f"border: {border_width}px solid {color_hex};"
            f" border-style: inset; "
            f"}}"
        )

    def sizeHint(self) -> QSize:
        width, height = 0, 0
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget():  # Check if the item is a widget
                widget_size_hint = item.widget().sizeHint()
                width += widget_size_hint.width()
                height = max(height, widget_size_hint.height())
        return QSize(width, height)

    ### CREATE LABELS ###

    def resize_turns_box(self) -> None:
        button_size = self.turns_panel.turns_tab.section.width() // 20

        for (
            button
        ) in (
            self.header_widget.turns_box.prop_rot_dir_button_manager.prop_rot_dir_buttons
        ):
            button.setMinimumSize(button_size, button_size)
            button.setMaximumSize(button_size, button_size)
            button.setIconSize(button.size() * 0.9)

        self.header_widget.setMinimumHeight(button_size)
        self.turns_widget.resize_turns_widget()
