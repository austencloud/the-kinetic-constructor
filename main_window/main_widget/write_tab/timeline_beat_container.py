# timeline_beat_widget.py
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.write_tab.timeline_blank_pictograph import (
    TimelineBlankPictograph,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_row import TimelineRow
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView
    from main_window.main_widget.main_widget import MainWidget


# timeline_beat_container.py
class TimelineBeatContainer(QFrame):
    def __init__(self, timeline_row: "TimelineRow", main_widget: "MainWidget") -> None:
        super().__init__(timeline_row)
        self.timeline_row = timeline_row
        self.main_widget = main_widget
        self.pictograph_view: Optional["BeatView"] = None
        self.blank_pictograph: "TimelineBlankPictograph" = None

        self._setup_ui()
        self.setAcceptDrops(True)
        self.set_blank_pictograph()

    def _setup_ui(self):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def set_blank_pictograph(self):
        """Set a blank pictograph in the beat."""
        self.blank_pictograph = TimelineBlankPictograph(self, self.main_widget)
        self.set_pictograph(self.blank_pictograph.view)

    def set_pictograph(self, pictograph_view: "BeatView"):
        self.pictograph_view = pictograph_view
        for i in reversed(range(self.layout.count())):
            widget = self.layout.takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.layout.addWidget(pictograph_view)

    def resize_timeline_beat_container(self):
        # Calculate size based on timeline_row's timeline size
        timeline_width = self.timeline_row.timeline.width()
        beat_size = int(timeline_width / 10)  # Adjust the divisor for size proportions
        self.setFixedSize(beat_size, beat_size)
        # Update the pictograph size
        self.pictograph_view.setFixedSize(beat_size, beat_size)

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Trigger resize when the beat container is resized
        self.resize_timeline_beat_container()
        super().resizeEvent(event)
