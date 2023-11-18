from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graphboard.graphboard import GraphBoard
    from widgets.sequence.sequence import Sequence


class SequenceButtons(QFrame):
    def __init__(
        self, main_widget: "MainWidget", graphboard: "GraphBoard", sequence: "Sequence"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graphboard = graphboard
        self.sequence = sequence

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.layout.addWidget(self.clear_sequence_button)
    
    def update_size(self) -> None:
        self.button_height = int(self.main_widget.height() * 1 / 20)
        self.setFixedHeight(self.button_height)
        self.clear_sequence_button.setFixedHeight(self.button_height)

