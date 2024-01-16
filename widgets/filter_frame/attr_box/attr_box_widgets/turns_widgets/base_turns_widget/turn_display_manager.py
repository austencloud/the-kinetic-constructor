from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.filter_frame.attr_box.base_attr_box import BaseAttrBox
    from .base_turns_widget import TurnsWidget


class TurnDisplayManager:
    def __init__(self, parent_widget: "TurnsWidget", attr_box: QFrame) -> None:
        self.parent_widget = parent_widget
        self.attr_box: BaseAttrBox = attr_box

    def setup_display_components(self) -> None:
        self.setup_turns_display()
        self.setup_turns_label()
        self.setup_turns_display_with_label_frame()
        self.add_turns_display_to_layout()

    def setup_turns_display_with_label_frame(self) -> None:
        self.turns_display_with_label_frame = QFrame()
        self.turns_display_with_label_frame_vbox = QVBoxLayout(
            self.turns_display_with_label_frame
        )
        self.turns_display_with_label_frame_vbox.setContentsMargins(0, 0, 0, 0)
        self.turns_display_with_label_frame_vbox.setSpacing(0)
        self.turns_display_with_label_frame_vbox.addWidget(
            self.parent_widget.turns_label
        )
        self.turns_display_with_label_frame_vbox.addWidget(self.turns_display)

    def setup_turns_display(self) -> None:
        self.turns_display = QLabel("0", self.parent_widget)
        self.turns_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_display.setStyleSheet(self._get_turns_display_style_sheet())
        self.turns_display.setFont(QFont("Arial"))
        self.turn_display_with_buttons_frame: QFrame = QFrame()
        self.hbox_with_turn_display_and_buttons: QHBoxLayout = QHBoxLayout(
            self.turn_display_with_buttons_frame
        )

    def setup_turns_label(self) -> None:
        self.parent_widget.turns_label = QLabel("Turns", self.parent_widget)
        self.parent_widget.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display.setText(str(turns))

    def _get_turns_display_style_sheet(self) -> str:
        return """
            QLabel {
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel:hover {
                background-color: #e5e5e5;
            }
        """

    def update_turnbox_size(self) -> None:
        """Update the size of the turns display for motion type."""
        turns_display = self.turns_display
        self.spacing = self.attr_box.attr_panel.height() // 250
        border_radius = min(turns_display.width(), turns_display.height()) * 0.25

        turns_display_font_size = int(self.attr_box.height() / 8)
        turns_display.setMinimumHeight(int(self.attr_box.height() / 3))
        turns_display.setMaximumHeight(int(self.attr_box.height() / 3))
        turns_display.setMinimumWidth(int(self.attr_box.height() / 3))
        turns_display.setMaximumWidth(int(self.attr_box.height() / 3))

        turns_display.setFont(
            QFont("Arial", turns_display_font_size, QFont.Weight.Bold)
        )
        turns_display.setStyleSheet(
            f"""
            QLabel {{
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def update_adjust_turns_button_size(self) -> None:
        for button in self.parent_widget.turn_adjustment_manager.adjust_turns_buttons:
            button_size = self.calculate_adjust_turns_button_size()
            button.update_attr_box_adjust_turns_button_size(button_size)

    def add_turns_display_to_layout(self) -> None:
        negative_buttons_frame = (
            self.parent_widget.turn_adjustment_manager.negative_buttons_frame
        )
        positive_buttons_frame = (
            self.parent_widget.turn_adjustment_manager.positive_buttons_frame
        )
        self.hbox_with_turn_display_and_buttons.setContentsMargins(0, 0, 0, 0)
        self.hbox_with_turn_display_and_buttons.setSpacing(0)
        self.hbox_with_turn_display_and_buttons.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.hbox_with_turn_display_and_buttons.addWidget(negative_buttons_frame)
        self.hbox_with_turn_display_and_buttons.addWidget(
            self.turns_display_with_label_frame
        )
        self.hbox_with_turn_display_and_buttons.addWidget(positive_buttons_frame)

        self.parent_widget.vbox_layout.addWidget(self.turn_display_with_buttons_frame)

    def calculate_adjust_turns_button_size(self) -> int:
        return int(self.attr_box.height() / 6)
