from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout, QFrame
from PyQt6.QtCore import Qt, QSize

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
        # Clear the layout first
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        # Retrieve the current layout configuration
        self.rows, self.cols = self.tab.current_layout
        num_beats = self.tab.current_num_beats

        # Add beat views including the start position
        index = 0
        for row in range(self.rows):
            for col in range(self.cols + 1):  # Include column 0 for the StartPositionBeatView
                if col == 0:
                    # Add the StartPositionBeatView in the first column of each row
                    if row == 0:
                        start_pos_view = StartPositionBeatView(self)
                        start_pos_view.setFixedSize(self._calculate_cell_size())
                        self.layout.addWidget(start_pos_view, row, col)
                elif index < num_beats:
                    # Add beat views in subsequent columns
                    beat_view = LayoutPreviewBeatView(self, number=index + 1)
                    beat_view.setFixedSize(self._calculate_cell_size())
                    self.layout.addWidget(beat_view, row, col)
                    index += 1


    def resizeEvent(self, event):
        """Recalculate cell sizes when the frame is resized."""
        super().resizeEvent(event)
        cell_size = self._calculate_cell_size()
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.setFixedSize(cell_size)

    def _calculate_cell_size(self) -> QSize:
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
