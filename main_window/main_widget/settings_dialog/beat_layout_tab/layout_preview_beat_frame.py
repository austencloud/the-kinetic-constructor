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
from main_window.main_widget.settings_dialog.beat_layout_tab.layout_preview_beat_view import (
    LayoutPreviewBeatView,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.beat_layout_tab import (
        BeatLayoutTab,
    )


class LayoutPreviewBeatFrame(QFrame):
    """Displays a live preview of the selected beat layout options."""

    rows = 0
    cols = 0
    current_num_beats = 16
    beat_views: dict[Union[int, str], BeatView] = {}

    def __init__(self, tab: "BeatLayoutTab"):
        super().__init__(tab)
        self.tab = tab
        self.sequence_widget = tab.sequence_widget
        self.main_widget = self.sequence_widget.main_widget
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_preview()

    def update_preview(self):
        """Rebuild the preview based on the current layout."""
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        self.rows, self.cols = self.tab.current_layout
        num_beats = self.tab.current_num_beats

        index = 0
        for row in range(self.rows):
            for col in range(self.cols + 1):
                if col == 0:
                    if row == 0:
                        start_pos_view = StartPositionBeatView(self)
                        start_pos = StartPositionBeat(self)
                        start_pos_view.set_start_pos(start_pos)
                        start_pos.grid.hide()
                        start_pos_view.setFixedSize(self._calculate_beat_size())
                        self.layout.addWidget(start_pos_view, row, col)
                        self.beat_views["start"] = start_pos_view
                elif index < num_beats:
                    beat_view = LayoutPreviewBeatView(self, number=index + 1)
                    beat = Beat(self)
                    beat_view.set_beat(beat, index + 1)
                    beat.grid.hide()
                    beat_view.setFixedSize(self._calculate_beat_size())
                    self.layout.addWidget(beat_view, row, col)
                    self.beat_views[index] = beat_view
                    index += 1

    def resizeEvent(self, event):
        """Recalculate cell sizes when the frame is resized."""
        super().resizeEvent(event)
        cell_size = self._calculate_beat_size()
        for beat_view in self.beat_views.values():
            beat_view.setFixedSize(cell_size)

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
