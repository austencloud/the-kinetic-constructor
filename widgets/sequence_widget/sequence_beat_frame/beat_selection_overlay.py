from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import QRect, Qt
from typing import TYPE_CHECKING, Optional

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView
if TYPE_CHECKING:

    from widgets.sequence_widget.sequence_widget import SequenceWidget


class BeatSelectionOverlay(QWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.selected_beat_view: Optional[BeatView] = None
        self.border_color = QColor("gold")
        self.border_width = 4  # Adjust as needed
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat(self, beat_view: BeatView):
        if self.selected_beat_view == beat_view:
            self.deselect_beat()
        else:
            if self.selected_beat_view:
                self.selected_beat_view.deselect()
            self.selected_beat_view = beat_view
            beat_view.select()
            self.update_overlay_position()
            self.show()

    def deselect_beat(self):
        if self.selected_beat_view:
            self.selected_beat_view.deselect()
        self.selected_beat_view = None
        self.hide()

    def update_overlay_position(self):
        if self.selected_beat_view:
            self.setGeometry(self.selected_beat_view.geometry())
            self.raise_()  # Ensure the overlay is above the selected beat view
            self.update()

    def paintEvent(self, event):
        if not self.selected_beat_view:
            return

        painter = QPainter(self)
        pen = QPen(self.border_color, self.border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        rect = self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2,
        )
        painter.drawRect(rect)
