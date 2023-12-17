from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame
from widgets.sequence_widget.button_frame import ButtonFrame
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = main_widget.graph_editor_widget.graph_editor.main_pictograph
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.beat_frame = BeatFrame(self.main_widget, self.pictograph, self)
        self.button_frame = ButtonFrame(self.main_widget, self.pictograph, self)
        self.beats = self.beat_frame.beats

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(self.layout.alignment() | Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.beat_frame)
        self.layout.addWidget(self.button_frame)

    def resize_sequence_widget(self) -> None:
        # The total width available for BeatViews and StartPositionView
        total_width = self.width()

        # Calculate the width for each BeatView based on the SequenceWidget width
        # while accommodating for the 5 columns (4 BeatViews and 1 StartPositionView)
        beat_view_width = int(total_width / self.beat_frame.COLUMN_COUNT)
        # Ensure that the height respects the aspect ratio of 90:75
        beat_view_height = int(beat_view_width * 90 / 75)

        # Apply the size constraints to the BeatViews
        for beat_view in self.beat_frame.beats:
            beat_view.setMaximumSize(beat_view_width, beat_view_height)

        # Apply the same size constraints to the StartPositionView
        self.beat_frame.start_position_view.setMaximumSize(
            beat_view_width, beat_view_height
        )

        # Update the layout to reflect the changes
        self.layout.update()
