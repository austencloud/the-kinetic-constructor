from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional

from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from .beat_view import BeatView

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWorkbenchBeatFrame


class BeatSelectionOverlay(QWidget):
    def __init__(self, beat_frame: "SequenceWorkbenchBeatFrame"):
        super().__init__(beat_frame)
        self.selected_beat: Optional[BeatView | StartPositionBeatView] = None
        self.border_color = QColor("gold")
        self.border_width = 4
        self.beat_frame = beat_frame
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat(self, beat_view: BeatView, toggle_animation=True, defer_show=True):
        if self.selected_beat == beat_view:
            return

        if self.selected_beat:
            self.deselect_beat()

        self.selected_beat = beat_view
        self.selected_beat.is_selected = True

        self.update_overlay_position()

        self.show()

        self._update_graph_editor(toggle_animation)

        beat_view.setCursor(Qt.CursorShape.ArrowCursor)

    def _safe_show(self):
        """Safely show the widget without interrupting animations."""
        if not self.isVisible():
            self.show()

    def _update_graph_editor(self, toggle_animation: bool = False):
        """Update graph editor components."""
        graph_editor = (
            self.selected_beat.beat_frame.main_widget.sequence_widget.graph_editor
        )
        graph_editor.pictograph_container.update_pictograph(self.selected_beat.beat)
        graph_editor.adjustment_panel.update_turns_panel()
        graph_editor.adjustment_panel.update_adjustment_panel()

        if toggle_animation and not graph_editor.is_toggled:
            graph_editor.animator.toggle()

    def deselect_beat(self):
        if self.selected_beat:
            self.selected_beat.is_selected = False
            self.selected_beat.setCursor(Qt.CursorShape.PointingHandCursor)
            self.selected_beat.update()

        self.selected_beat = None

        self.hide()

    def update_overlay_position(self):
        if self.selected_beat:
            self.setGeometry(self.selected_beat.geometry())
            self.raise_()
            # self.update()

    def get_selected_beat(self) -> Optional[BeatView]:
        return self.selected_beat

    def paintEvent(self, event):
        if not self.selected_beat:
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
        painter.end()
