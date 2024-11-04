from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.option_picker.option_picker import (
        OptionPicker,
    )


class ChooseYourNextPictographLabel(QLabel):
    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def set_default_text(self) -> None:
        self.setText("Choose your next pictograph:")

    def set_text_to_loading(self) -> None:
        self.setText("Loading...")

    def set_stylesheet(self) -> None:
        height = self.option_picker.height()
        font_size = int(0.04 * height)
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.height() // 2}px;"
            f"  font-size: {font_size}px;"
            f"  font-family: 'Monotype Corsiva';"
            f"}}"
        )

    def resize_choose_your_next_pictograph_label(self) -> None:
        # use font metrics to get the width and height, allowing for a margin
        font_metrics = self.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self.text())
        text_height = font_metrics.height()
        margin = 20
        width = text_width + margin
        height = text_height + margin
        self.setFixedSize(width, height)
        self.set_stylesheet()
