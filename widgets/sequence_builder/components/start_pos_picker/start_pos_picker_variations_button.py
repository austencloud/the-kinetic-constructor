from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QFont, QEnterEvent
from PyQt6.QtCore import QSize, Qt

from .start_pos_manager import StartPosManager
from ....pictograph.pictograph import Pictograph

from widgets.sequence_builder.components.start_pos_picker.start_pos_pictograph_frame import (
    StartPosPickerPictographFrame,
)
from ....scroll_area.components.start_pos_picker_pictograph_factory import (
    StartPosPickerPictographFactory,
)
from .choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder
    from widgets.sequence_builder.components.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )


class StartPosVariationsButton(QPushButton):
    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.setText("Variations")
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #446CB3;
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3D5C99;
            }
        """
        )

    def resize_variations_button(self):
        width = self.start_pos_picker.width() // 5
        height = self.start_pos_picker.height() // 10
        self.setFixedSize(width, height)
        font_size = int(width // 10)
        self.setFont(QFont("Calibri", font_size, italic=True))

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_label_style(outline=True)

    def leaveEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_label_style()

    def set_label_style(self, outline=False) -> None:
        width = self.width() // 30
        border_style = f"{width}px solid gold" if outline else "none"
        self.setStyleSheet(
            f"QPushButton {{"
            f"  background-color: #446CB3;"
            f"  color: white;"
            f"  border-radius: 10px;"
            f"  padding: 10px;"
            f"  margin-top: 10px;"
            f"  margin-bottom: 10px;"
            f"  border: {border_style};"
            f"}}"
        )
