from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import (
    StartPositionBeatView,
)

if TYPE_CHECKING:

    from widgets.sequence_widget.sequence_widget import SequenceWidget


class BeatSelectionManager(QWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.selected_beat_view: Optional[BeatView | StartPositionBeatView] = None
        self.border_color = QColor("gold")
        self.border_width = 4  # Adjust as needed
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat(self, beat_view: BeatView):
        if self.selected_beat_view == beat_view:
            return
        else:
            if self.selected_beat_view:
                self.selected_beat_view.deselect()
            self.selected_beat_view = beat_view
            blue_turns = self.selected_beat_view.beat.blue_motion.turns
            red_turns = self.selected_beat_view.beat.red_motion.turns
            self.selected_beat_view.is_selected = True
            graph_editor = (
                self.selected_beat_view.beat_frame.sequence_widget.sequence_modifier.graph_editor
            )
            graph_editor.update_GE_pictgraph(self.selected_beat_view.beat)

            graph_editor.adjustment_panel.update_turns_panel(blue_turns, red_turns)
            graph_editor.adjustment_panel.update_adjustment_panel()
            self.update()
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
            self.raise_()
            self.update()

    def get_selected_beat(self) -> Optional[BeatView]:
        return self.selected_beat_view

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
