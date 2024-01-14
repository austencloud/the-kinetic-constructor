from PyQt6.QtWidgets import QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
        BaseTurnsWidget,
    )


class DisplayTurnsManager:
    def __init__(self, base_turns_widget: "BaseTurnsWidget", attr_box: QFrame) -> None:
        self.base_turns_widget = base_turns_widget
        self.attr_box = attr_box

    def setup_display_components(self):
        self.setup_turns_display()
        self.setup_turns_label()

    def setup_turns_display(self):
        self.base_turns_widget.turns_display = QLabel("0", self.base_turns_widget)
        self.base_turns_widget.turns_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.base_turns_widget.turns_display.setStyleSheet(
            self._get_turns_display_style_sheet()
        )
        self.base_turns_widget.turns_display.setFont(QFont("Arial", 16))

    def setup_turns_label(self):
        self.base_turns_widget.turns_label = QLabel("Turns", self.base_turns_widget)
        self.base_turns_widget.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.base_turns_widget.turns_display.setText(str(turns))

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
        self.spacing = self.attr_box.attr_panel.height() // 250
        border_radius = (
            min(
                self.base_turns_widget.turns_display.width(),
                self.base_turns_widget.turns_display.height(),
            )
            * 0.25
        )
        turns_display_font_size = int(self.attr_box.height() / 8)

        self.base_turns_widget.turns_display.setMinimumHeight(
            int(self.attr_box.height() / 3)
        )
        self.base_turns_widget.turns_display.setMaximumHeight(
            int(self.attr_box.height() / 3)
        )
        self.base_turns_widget.turns_display.setMinimumWidth(
            int(self.attr_box.height() / 3)
        )
        self.base_turns_widget.turns_display.setMaximumWidth(
            int(self.attr_box.height() / 3)
        )
        self.base_turns_widget.turns_display.setFont(
            QFont("Arial", turns_display_font_size, QFont.Weight.Bold)
        )

        # Adjust the stylesheet to match the combo box style without the arrow
        self.base_turns_widget.turns_display.setStyleSheet(
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
        for button in self.base_turns_widget.adjust_turns_manager.adjust_turns_buttons:
            button_size = self.calculate_adjust_turns_button_size()
            button.update_attr_box_adjust_turns_button_size(button_size)

    def calculate_adjust_turns_button_size(self) -> int:
        return int(self.attr_box.height() / 6)
