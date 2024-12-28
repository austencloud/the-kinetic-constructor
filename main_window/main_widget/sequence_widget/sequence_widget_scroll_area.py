from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea

if TYPE_CHECKING:
    from .sequence_widget import SequenceWidget


class SequenceWidgetScrollArea(QScrollArea):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea{background: transparent;}")
        self.setFrameShape(QScrollArea.Shape.NoFrame)
