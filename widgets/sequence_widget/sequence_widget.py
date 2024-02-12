import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.pictograph.pictograph import Pictograph
from widgets.sequence_widget.beat_frame.beat_frame import SequenceBeatFrame
from widgets.sequence_widget.button_frame import SequenceButtonFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.beat_frame = SequenceBeatFrame(self.main_widget, self)
        self.button_frame = SequenceButtonFrame(self)
        self.beats = self.beat_frame.beats

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        self.layout.addWidget(self.beat_frame)
        self.layout.addWidget(self.button_frame)

    def save_sequence(sequence: list[Pictograph], filename: str) -> None:
        sequence_data = [pictograph.get.pictograph_dict() for pictograph in sequence]
        with open(filename, "w") as file:
            json.dump(sequence_data, file, indent=4)

    def resize_sequence_widget(self) -> None:
        beat_view_height = int(self.height() * 0.9 / self.beat_frame.ROW_COUNT)
        beat_view_width = beat_view_height
        for beat_view in self.beat_frame.beats:
            beat_view.setMaximumSize(beat_view_width, beat_view_height)
            beat_view.setMinimumSize(beat_view_width, beat_view_height)
        self.beat_frame.start_pos_view.setMinimumSize(beat_view_width, beat_view_height)
        self.beat_frame.start_pos_view.setMaximumSize(beat_view_width, beat_view_height)
        self.layout.update()
        minimum_width = int(self.main_widget.width() * 2 / 5)
        self.setMinimumWidth(minimum_width)
