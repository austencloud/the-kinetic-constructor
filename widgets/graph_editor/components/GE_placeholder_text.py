from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .GE_adjustment_panel import GE_AdjustmentPanel


class GE_PlaceHolderTextLabel(QLabel):
    def __init__(self, adjustment_panel: "GE_AdjustmentPanel") -> None:
        super().__init__(adjustment_panel)
        self.option_picker = adjustment_panel
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def set_default_text(self):
        self.setText(
            "This is where you'll modify each pictograph.\nSelect a start position to begin!\n--->"
        )

    def set_text_to_loading(self):
        self.setText("Loading...")

    def set_stylesheet(self) -> None:
        width = self.option_picker.width()
        font_size = int(0.02 * width)
        self.setFont(QFont("Cambria", font_size))
        self.show()
