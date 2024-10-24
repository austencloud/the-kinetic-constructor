# timeline_beat_widget.py
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.act_beat_view import ActBeatView
from main_window.main_widget.write_tab.timeline_blank_pictograph import (
    TimelineBlankPictograph,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_row import TimelineRow
    from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
    from main_window.main_widget.main_widget import MainWidget


class TimelineBeatContainer(QFrame):
    def __init__(
        self, timeline_row: "TimelineRow", main_widget: "MainWidget", row_number: int
    ) -> None:
        super().__init__(timeline_row)
        self.timeline_row = timeline_row
        self.main_widget = main_widget
        self.row_number = row_number
        self.act_beat_view: Optional["ActBeatView"] = None

        self._setup_ui()
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
        self.act_beat_view = ActBeatView(
            self.timeline_row.timeline.write_tab.beat_frame, self.row_number
        )
        self.set_pictograph(self.act_beat_view)

    def set_pictograph(self, pictograph_view: "ActBeatView"):
        """Replace the current pictograph with a new one."""
        self.act_beat_view = pictograph_view
        for i in reversed(range(self.layout.count())):
            widget = self.layout.takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.layout.addWidget(pictograph_view)

    # timeline_beat_container.py
    def resize_timeline_beat_container(self):
        """Resize beat container based on timeline width."""
        timeline_width = self.timeline_row.timeline.width()
        beat_size = int(timeline_width / 9)  # Adjust the divisor for size proportions
        self.setFixedSize(beat_size, beat_size)
        self.act_beat_view.setFixedSize(beat_size, beat_size)

        # Rescale the beat view to fit the container
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.act_beat_view.resetTransform()
        self.act_beat_view.scale(self.view_scale, self.view_scale)

        print(
            f"Resized beat container for row {self.row_number} to {beat_size}px"
        )

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Trigger resize when the beat container is resized."""
        self.resize_timeline_beat_container()
        super().resizeEvent(event)
