from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional

from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from .beat_view import BeatView

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatSelectionOverlay(QWidget):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        super().__init__(beat_frame)
        self.selected_beat: Optional[BeatView | StartPositionBeatView] = None
        self.border_color = QColor("gold")
        self.border_width = 4
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat(self, beat_view: BeatView):
        if self.selected_beat == beat_view:
            return
        else:
            if self.selected_beat:
                self.selected_beat.deselect()
            self.selected_beat = beat_view
            blue_motion = self.selected_beat.beat.blue_motion
            red_motion = self.selected_beat.beat.red_motion
            self.selected_beat.is_selected = True
            graph_editor = (
                self.selected_beat.beat_frame.main_widget.sequence_widget.graph_editor
            )

            self.update()
            self.update_overlay_position()
            self.show()

            graph_editor.pictograph_container.update_GE_pictograph(
                self.selected_beat.beat
            )
            graph_editor.adjustment_panel.update_turns_panel(blue_motion, red_motion)
            graph_editor.adjustment_panel.update_adjustment_panel()
            if isinstance(beat_view, StartPositionBeatView):
                start_pos_pictograph = beat_view.beat
                blue_start_pos_ori_picker = (
                    graph_editor.adjustment_panel.blue_ori_picker
                )
                red_start_pos_ori_picker = graph_editor.adjustment_panel.red_ori_picker

                blue_start_pos_ori_picker.ori_picker_widget.ori_setter.set_initial_orientation(
                    start_pos_pictograph, "blue"
                )
                red_start_pos_ori_picker.ori_picker_widget.ori_setter.set_initial_orientation(
                    start_pos_pictograph, "red"
                )
            # QApplication.processEvents()

    def deselect_beat(self):
        if self.selected_beat:
            self.selected_beat.deselect()
        self.selected_beat = None
        self.hide()

    def update_overlay_position(self):
        if self.selected_beat:
            self.setGeometry(self.selected_beat.geometry())
            self.raise_()
            self.update()

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
