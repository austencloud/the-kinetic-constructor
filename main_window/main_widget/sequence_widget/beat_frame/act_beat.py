# write_tab_beat.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem, QGraphicsScene
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_row import TimelineRow
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView
    from main_window.main_widget.main_widget import MainWidget

class ActBeatView(QGraphicsView):
    def __init__(self, main_widget: "MainWidget", number=None):
        super().__init__()
        self.main_widget = main_widget
        self.number = number  # Beat number to display
        self.scene:QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.beat_number_item = None
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none; border: 1px solid black;")
        self._setup_blank_beat()
        self.resize_beat_view()

    def _setup_blank_beat(self):
        """Set up the blank beat, adding beat number display."""
        self.add_beat_number()

    def add_beat_number(self, beat_number_text=None):
        """Display the beat number."""
        if not beat_number_text:
            beat_number_text = str(self.number) if self.number else "N/A"

        if self.beat_number_item:
            self.scene.removeItem(self.beat_number_item)

        self.beat_number_item = QGraphicsTextItem(beat_number_text)
        self.beat_number_item.setFont(QFont("Georgia", 24))  # Adjust font size as needed
        self.beat_number_item.setPos(QPointF(10, 10))  # Adjust position as needed
        self.scene.addItem(self.beat_number_item)

    def resize_beat_view(self):
        """Resize the beat view to fit the container."""
        self.setFixedSize(100, 100)  # Adjust size based on your design

    def clear_beat(self):
        """Clear the beat from the view."""
        self.scene.clear()
        self._setup_blank_beat()
