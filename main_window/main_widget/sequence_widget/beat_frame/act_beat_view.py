# write_tab_beat.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QFont

from main_window.main_widget.sequence_widget.beat_frame.act_beat import ActBeat


if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_beat_frame import ActBeatFrame

# write_tab_beat.py
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem, QGraphicsScene
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont


class ActBeatView(QGraphicsView):
    def __init__(self, beat_frame: "ActBeatFrame", number=None):
        super().__init__()
        self.beat_frame = beat_frame
        self.number = number  # Beat number to display
        self.beat = ActBeat(beat_frame, 1)
        self.setScene(self.beat)
        self.beat_number_item = None
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none; border: 1px solid black;")

        # Disable both scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Prevent scrolling by disabling scrolling behavior
        self.setInteractive(False)

        self._setup_blank_beat()

    def _setup_blank_beat(self):
        """Set up the blank beat, adding beat number display."""
        self.add_beat_number()

    def add_beat_number(self, beat_number_text=None):
        """Display the beat number."""
        if not beat_number_text:
            beat_number_text = str(self.number) if self.number else "N/A"

        if self.beat_number_item:
            self.beat.removeItem(self.beat_number_item)

        self.beat_number_item = QGraphicsTextItem(beat_number_text)
        self.beat_number_item.setFont(QFont("Georgia", 24))
        self.beat_number_item.setPos(QPointF(10, 10))  # Adjust position as needed
        self.beat.addItem(self.beat_number_item)

    def resize_act_beat_view(self):
        """Resize the beat view to fit the container."""
        # size = int(self.beat_frame.write_tab.width() * 0.15)
        # self.setFixedSize(size, size)

        # Rescale the beat view to fit the container
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def clear_beat(self):
        """Clear the beat from the view."""
        self.beat.clear()
        self._setup_blank_beat()

    def wheelEvent(self, event):
        """Override to prevent scrolling."""
        self.beat_frame.wheelEvent(event)
