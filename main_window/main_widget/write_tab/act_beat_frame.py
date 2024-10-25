# act_beat_frame.py
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from main_window.main_widget.sequence_widget.beat_frame.act_beat_view import ActBeatView

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class ActBeatFrame(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__()
        self.write_tab = write_tab
        self.main_widget = write_tab.main_widget
        self.beat_views: List[ActBeatView] = []
        self.timestamps: List[QLabel] = []  # Holds timestamp labels
        self._setup_layout()

    def _setup_layout(self):
        # Using a grid layout for both timestamps and beats
        self.layout: QGridLayout = QGridLayout(self)
        self.setLayout(self.layout)

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a large grid of beats."""
        for row in range(num_rows):
            # Add timestamp for each row
            timestamp = QLabel(f"{row * 10}:00")  # Example: 0:00, 0:10, etc.
            self.timestamps.append(timestamp)
            self.layout.addWidget(timestamp, row, 0)  # Align in the first column

            # Add beats for the row
            for col in range(1, num_beats + 1):
                beat_view = ActBeatView(self, number=(row * num_beats) + col)
                self.beat_views.append(beat_view)
                self.layout.addWidget(beat_view, row, col)

    def resizeEvent(self, event):
        """Resize each beat and adjust layout dynamically."""
        for view in self.beat_views:
            view.resize_act_beat_view()
        super().resizeEvent(event)
