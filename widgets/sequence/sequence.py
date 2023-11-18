from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.sequence.sequence_buttons import SequenceButtons
from widgets.sequence.sequence_beats import SequenceBeats


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graphboard.graphboard import GraphBoard


class Sequence(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graphboard = main_widget.graph_editor.graphboard
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.beats = SequenceBeats(self.main_widget, self.graphboard, self)
        self.buttons = SequenceButtons(self.main_widget, self.graphboard, self)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.layout.addWidget(self.beats)
        self.layout.addWidget(self.buttons)

    def update_size(self) -> None:
        self.buttons.update_size()
        self.beats.update_size()
