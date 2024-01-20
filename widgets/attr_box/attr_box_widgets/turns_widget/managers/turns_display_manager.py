from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from ..turns_widget import TurnsWidget


class TurnDisplayManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.attr_box: AttrBox = turns_widget.attr_box

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
            self.turns_widget.turns_label
        )
        self.turns_display_with_label_frame_vbox.addWidget(self.turns_display)

    def setup_turns_display(self) -> None:
        self.turns_display = QLabel("0", self.turns_widget)
        self.turns_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_display.setStyleSheet(self._get_turns_display_style_sheet())
        self.turns_display.setFont(QFont("Arial"))
        self.turn_display_with_buttons_frame: QFrame = QFrame()
        self.hbox_with_turn_display_and_buttons: QHBoxLayout = QHBoxLayout(
            self.turn_display_with_buttons_frame
        )

    def setup_turns_label(self) -> None:
        self.turns_widget.turns_label = QLabel("Turns", self.turns_widget)
        self.turns_widget.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def update_turn_display(self) -> None:
        """Update the size of the turns display for motion type."""
        self.resize_turn_display()
        self.set_turn_display_styles()

    def set_turn_display_styles(self) -> None:
        self.turns_display_font_size = int(self.attr_box.attr_panel.width() / 34)
        self.turns_display.setFont(
            QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold)
        )
        border_radius = (
            min(self.turns_display.width(), self.turns_display.height()) * 0.25
        )
        self.turns_display.setStyleSheet(
            f"""
            QLabel {{
                border: {self.attr_box.turn_display_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def resize_turn_display(self) -> None:
        self.turns_display.setMinimumHeight(int(self.attr_box.attr_panel.width() / 18))
        self.turns_display.setMaximumHeight(int(self.attr_box.attr_panel.width() / 18))
        self.turns_display.setMinimumWidth(int(self.attr_box.attr_panel.width() / 14))
        self.turns_display.setMaximumWidth(int(self.attr_box.attr_panel.width() / 14))

    def update_adjust_turns_button_size(self) -> None:
        for button in self.turns_widget.button_manager.adjust_turns_buttons:
            button_size = self.calculate_adjust_turns_button_size()
            button.update_adjust_turns_button_size(button_size)

    def add_turns_display_to_layout(self) -> None:
        negative_buttons_frame = self.turns_widget.button_manager.negative_buttons_frame
        positive_buttons_frame = self.turns_widget.button_manager.positive_buttons_frame
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

        self.turns_widget.vbox_layout.addWidget(self.turn_display_with_buttons_frame)

    def calculate_adjust_turns_button_size(self) -> int:
        return int(self.attr_box.attr_panel.width() / 25)
