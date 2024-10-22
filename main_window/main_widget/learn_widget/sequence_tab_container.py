from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceTabContainer(QWidget):
    def __init__(
        self, sequence_widget: "SequenceWidget", stacked_widget: QStackedWidget
    ):
        super().__init__()

        self.sequence_widget = sequence_widget
        self.stacked_widget = stacked_widget

        self.layout:QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.stacked_widget)

        self.layout.setStretch(0, 1)  
        self.layout.setStretch(1, 1)  