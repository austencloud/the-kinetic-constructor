from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import BLUE, HEX_BLUE, HEX_RED
from widgets.graph_editor.components.adjustment_panel.turns_box.turns_widget.direct_set_dialog.GE_direct_set_adjustment_button import DirectSetAdjustmentButton


if TYPE_CHECKING:
    from widgets.graph_editor.components.adjustment_panel.turns_box.turns_widget.GE_turns_widget import GE_TurnsWidget

from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFrame


class GE_DirectSetDialog(QDialog):
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: 5px;
            }}
        """
        )
        self.direct_set_buttons: dict[str, QPushButton] = {}

        self._setup_layout()
        self._setup_buttons()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.adjustSize()

    def _setup_buttons(self):
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]

        for value in turns_values:
            button = DirectSetAdjustmentButton(value, self.turns_widget)
            button.set_button_styles()
            button.clicked.connect(
                lambda _, v=value: self.select_turns(float(v) if "." in v else int(v))
            )
            self.layout.addWidget(button)

    def select_turns(self, value):
        self.turns_widget.adjustment_manager.direct_set_turns(value)
        self.accept()

    def setup_direct_set_buttons(self) -> None:
        self.turns_buttons_frame = QFrame()
        self.turns_buttons_layout = QHBoxLayout(self.turns_buttons_frame)
        self.turns_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        for value in turns_values:
            button = QPushButton(value, self.turns_widget)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #c0c0c0;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e5e5e5;
                    border-color: #a0a0a0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """
            )
            button.clicked.connect(
                lambda _, v=value: self.turns_widget.adjustment_manager.direct_set_turns(
                    float(v) if v in ["0.5", "1.5", "2.5"] else int(v)
                )
            )
            self.direct_set_buttons[value] = button
            self.turns_buttons_layout.addWidget(button)



    def resize_direct_set_buttons(self) -> None:
        for button in self.direct_set_buttons.values():
            button.setMinimumWidth(int(self.turns_widget.width() / 2))
