from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGridLayout, QFrame
from PyQt6.QtCore import Qt, QSize

from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.layout_beat_view import (
    LayoutBeatView,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.beat_layout_tab import (
        BeatLayoutTab,
    )


class LayoutBeatFrame(QFrame):
    """Displays a live preview of the selected beat layout options."""

    rows = 0
    cols = 0
    current_num_beats = 16
    beat_views: list[Union[BeatView]] = []
    start_pos_view: StartPositionBeatView = None

    def __init__(self, tab: "BeatLayoutTab"):
        super().__init__(tab)
        self.tab = tab
        self.sequence_widget = tab.sequence_widget
        self.main_widget = self.sequence_widget.main_widget
        self._setup_layout()
        self._init_beats()
        self.update_preview()

    def _init_beats(self):
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)
        self.beat_views = [LayoutBeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beat_views:
            beat.hide()

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_preview(self):
        """Rebuild the preview based on the current layout."""
        self.cols, self.rows = self.tab.current_layout
        num_beats = self.tab.num_beats

        # Handle the start position beat view
        start_pos = StartPositionBeat(self)
        self.start_pos_view.set_start_pos(start_pos)
        start_pos.grid.hide()
        self.layout.addWidget(self.start_pos_view, 0, 0)
        self.start_pos_view.setVisible(True)

        index = 0
        for row in range(self.rows):
            for col in range(1, self.cols + 1):  # Start at column 1 for beat views
                if index < num_beats:
                    if index not in self.beat_views:
                        beat_view = self.beat_views[index]
                        beat = Beat(self)
                        beat_view.set_beat(beat, index + 1)
                        beat.grid.hide()
                        self.layout.addWidget(beat_view, row, col)
                        self.beat_views[index] = beat_view
                    else:
                        self.layout.addWidget(self.beat_views[index], row, col)
                    self.beat_views[index].setVisible(True)
                    index += 1

        for unused_index in range(index, len(self.beat_views)):
            if unused_index in self.beat_views:
                self.beat_views[unused_index].setVisible(False)

    def _calculate_beat_size(self) -> QSize:
        """Calculate the size of each beat view cell."""
        available_width = self.width() - self.layout.horizontalSpacing() * (
            self.cols + 1
        )
        available_height = self.height() - self.layout.verticalSpacing() * (
            self.rows + 1
        )
        cell_size = min(
            available_width // (self.cols + 1), available_height // (self.rows + 1)
        )
        return QSize(cell_size, cell_size)

    def resizeEvent(self, event):
        """Recalculate cell sizes when the frame is resized."""
        super().resizeEvent(event)
        cell_size = self._calculate_beat_size()
        for beat_view in self.beat_views:
            beat_view.setFixedSize(cell_size)
        self.start_pos_view.setFixedSize(cell_size)
