from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.sequence.sequence_buttons import SequenceButtons
from widgets.sequence.sequence_beats import SequenceBeats


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class Sequence(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = main_widget.graph_editor.pictograph
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.beat_frame = SequenceBeats(self.main_widget, self.pictograph, self)
        self.button_frame = SequenceButtons(self.main_widget, self.pictograph, self)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.beat_frame)
        self.layout.addWidget(self.button_frame)

    def update_size(self) -> None:
        self.button_frame.update_size()
        self.beat_frame.update_size()
