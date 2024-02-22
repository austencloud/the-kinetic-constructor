from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_ori_picker_widget import (
        GE_StartPosOriPickerWidget,
    )


class GE_StartPosOriPickerDisplayManager:
    def __init__(self, ori_picker_widget: "GE_StartPosOriPickerWidget") -> None:
        self.ori_picker_widget = ori_picker_widget
        self.graph_editor = (
            self.ori_picker_widget.ori_picker_box.adjustment_panel.graph_editor
        )

    def setup_display_components(self) -> None:
        self.ori_display = self._setup_ori_display()
        self.ori_display_frame = self._setup_ori_display_frame(self.ori_display)
        self.add_ori_display_to_layout()

    def _setup_ori_display_frame(self, ori_display) -> QFrame:
        ori_display_frame = QFrame()
        ori_display_frame_layout = QVBoxLayout(ori_display_frame)
        ori_display_frame_layout.setContentsMargins(2, 2, 2, 2)
        ori_display_frame_layout.setSpacing(2)
        ori_display_frame_layout.addWidget(ori_display)
        return ori_display_frame

    def _setup_ori_display(self) -> QLabel:
        ori_display = QLabel("0", self.ori_picker_widget)
        ori_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ori_display.setStyleSheet(self._get_ori_display_style_sheet())
        ori_display.setFont(QFont("Arial"))
        self.turn_display_with_buttons_frame: QFrame = QFrame()
        self.hbox_with_ori_display_and_buttons: QHBoxLayout = QHBoxLayout(
            self.turn_display_with_buttons_frame
        )
        return ori_display

    def update_ori_display(self, ori: Union[int, float]) -> None:
        self.ori_display.setText(str(ori))

    def _get_ori_display_style_sheet(self) -> str:
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

    def update_ori_picker_display(self) -> None:
        """Update the size of the ori display for motion type."""
        self.resize_ori_picker_display()
        self.set_ori_picker_display_styles()

    def set_ori_picker_display_styles(self) -> None:
        self.ori_display_font_size = int(self.graph_editor.width() / 36)
        self.ori_display.setFont(
            QFont("Arial", self.ori_display_font_size, QFont.Weight.Bold)
        )
        border_radius = min(self.ori_display.width(), self.ori_display.height()) / 4
        turn_display_border = int(self.ori_display.width() / 28)
        self.ori_display.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def resize_ori_picker_display(self) -> None:
        self.ori_display.setMinimumHeight(int(self.graph_editor.width() / 18))
        self.ori_display.setMaximumHeight(int(self.graph_editor.width() / 18))
        self.ori_display.setMinimumWidth(int(self.graph_editor.width() / 14))
        self.ori_display.setMaximumWidth(int(self.graph_editor.width() / 14))

    def add_ori_display_to_layout(self) -> None:

        self.hbox_with_ori_display_and_buttons.setContentsMargins(0, 0, 0, 0)
        self.hbox_with_ori_display_and_buttons.setSpacing(0)
        self.hbox_with_ori_display_and_buttons.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.hbox_with_ori_display_and_buttons.addWidget(self.ori_display_frame)

        self.ori_picker_widget.layout.addWidget(self.turn_display_with_buttons_frame)

    def calculate_adjust_ori_button_size(self) -> int:
        return int(self.graph_editor.width() / 25)

    def get_current_ori_value(self) -> int:
        return (
            int(self.ori_display.text())
            if self.ori_display.text() in ["0", "1", "2", "3"]
            else float(self.ori_display.text())
        )
