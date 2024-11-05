from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QFontMetrics
from data.constants import IN, COUNTER, OUT, CLOCK, HEX_BLUE, HEX_RED
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OriSelectionDialog(QDialog):
    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(
            ori_picker_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.ori_picker_widget = ori_picker_widget
        self.selected_orientation = None
        self.buttons: dict[str, QPushButton] = {}
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self):
        border_color = HEX_BLUE if self.ori_picker_widget.color == "blue" else HEX_RED
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {border_color};
                border-radius: 5px;
                background-color: white;
            }}
            """
        )

    def _setup_buttons(self):
        orientations = [IN, COUNTER, OUT, CLOCK]
        for orientation in orientations:
            button = QPushButton(orientation)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, ori=orientation: self.select_orientation(ori)
            )
            self.buttons[orientation] = button

        self.resize_buttons()

    def resize_buttons(self):
        """Resize buttons according to the orientation label's size."""
        ori_label_width = self.ori_picker_widget.clickable_ori_label.width()
        button_height = int(self.ori_picker_widget.ori_picker_box.height() // 3)
        font_size = int(button_height * 0.5)  # Font size based on button height

        font = QFont("Arial", font_size, QFont.Weight.Bold)
        font_metrics = QFontMetrics(font)

        for orientation, button in self.buttons.items():
            button.setFont(font)

            # Calculate button width based on text length
            text_width = font_metrics.horizontalAdvance(orientation)
            button_width = max(text_width + 40, ori_label_width // 2)  # Add padding
            border_width = button_height // 20
            button.setFixedSize(QSize(button_width, button_height))
            button.setStyleSheet(
                f"""
                QPushButton {{
                    border: {border_width}px solid {HEX_BLUE if self.ori_picker_widget.color == "blue" else HEX_RED};
                    border-radius: {button_height // 2}px;
                    background-color: #ffffff;
                }}
                QPushButton:hover {{
                    background-color: #f0f0f0;
                }}
                """
            )

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        for button in self.buttons.values():
            layout.addWidget(button)
        self.adjustSize()

    def select_orientation(self, orientation):
        self.selected_orientation = orientation
        self.accept()
