from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame
from widgets.sequence_widget.button_frame import ButtonFrame


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = main_widget.graph_editor.pictograph
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.beat_frame = BeatFrame(self.main_widget, self.pictograph, self)
        self.button_frame = ButtonFrame(self.main_widget, self.pictograph, self)
        self.beats = self.beat_frame.beats

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.beat_frame)
        self.layout.addWidget(self.button_frame)

    def resize_sequence_widget(self, event) -> None:
        self.beat_frame.resize_beat_frame()
        # self.button_frame.resize_letter_buttons()
