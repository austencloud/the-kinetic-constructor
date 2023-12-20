from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from constants.numerical_constants import RATIO
from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame
from widgets.sequence_widget.button_frame import ButtonFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = main_widget.graph_editor_tab.graph_editor.main_pictograph
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.beat_frame = BeatFrame(self.main_widget, self.pictograph, self)
        self.button_frame = ButtonFrame(self.main_widget, self.pictograph, self)
        self.beats = self.beat_frame.beats

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        self.layout.addWidget(self.beat_frame)
        self.layout.addWidget(self.button_frame)

    def resize_sequence_widget(self) -> None:
        beat_view_height = int(self.height() * 0.9 / self.beat_frame.ROW_COUNT)
        beat_view_width = int(beat_view_height * RATIO)

        for beat_view in self.beat_frame.beats:
            beat_view.setMaximumSize(beat_view_width, beat_view_height)
            beat_view.setMinimumSize(beat_view_width, beat_view_height)

        self.beat_frame.start_position_view.setMinimumSize(
            beat_view_width, beat_view_height
        )

        self.beat_frame.start_position_view.setMaximumSize(
            beat_view_width, beat_view_height
        )

        self.layout.update()
        self.setMaximumWidth(
            self.beat_frame.layout.sizeHint().width()
            + self.button_frame.layout.sizeHint().width()
        )
