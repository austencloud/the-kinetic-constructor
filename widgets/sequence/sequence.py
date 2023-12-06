from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.sequence.beat_view import BeatView
from widgets.sequence.sequence_buttons import SequenceButtons
from widgets.sequence.sequence_frame import SequenceFrame 


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class Sequence(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = main_widget.graph_editor.pictograph
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.frame = SequenceFrame(self.main_widget, self.pictograph, self)
        self.buttons = SequenceButtons(self.main_widget, self.pictograph, self)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.buttons)

    def update_size(self) -> None:
        self.buttons.update_size()
        self.frame.update_size()
        for beat in self.frame.findChildren(BeatView):
            beat.update_pictograph_size()
