from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.sequence.sequence import Sequence


class SequenceButtons(QFrame):
    def __init__(
        self, main_widget: "MainWidget", pictograph: "Pictograph", sequence: "Sequence"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = pictograph
        self.sequence = sequence
        self.button_height = int(self.main_widget.height() * 1 / 20)

        self.layout:QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.buttons.append(self.clear_sequence_button)

        self.layout.addWidget(self.clear_sequence_button)

    def update_size(self) -> None:
        self.setFixedHeight(self.button_height)
        self.clear_sequence_button.setFixedHeight(self.button_height)
