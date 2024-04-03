from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Optional
<<<<<<<< HEAD:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_manager.py

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import (
========
from widgets.sequence_widget.sequence_widget_beat_frame.beat import BeatView

from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
>>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_overlay.py
    StartPositionBeatView,
)

if TYPE_CHECKING:
<<<<<<<< HEAD:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_manager.py

    from widgets.sequence_widget.sequence_widget import SequenceWidget
========
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
>>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_overlay.py


class BeatSelectionManager(QWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.selected_beat: Optional[BeatView | StartPositionBeatView] = None
        self.border_color = QColor("gold")
        self.border_width = 4  # Adjust as needed
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def select_beat(self, beat_view: BeatView):
        if self.selected_beat == beat_view:
            return
        else:
            if self.selected_beat:
                self.selected_beat.deselect()
            self.selected_beat = beat_view
            blue_turns = self.selected_beat.beat.blue_motion.turns
            red_turns = self.selected_beat.beat.red_motion.turns
            self.selected_beat.is_selected = True
            graph_editor = (
                self.selected_beat.beat_frame.sequence_widget.sequence_modifier.graph_editor
            )
<<<<<<<< HEAD:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_manager.py
            graph_editor.update_GE_pictgraph(self.selected_beat.beat)
========

            self.update()
            self.update_overlay_position()
            self.show()
            graph_editor.update_GE_pictograph(self.selected_beat.beat)
            # QApplication.processEvents()
>>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409:widgets/sequence_widget/sequence_widget_beat_frame/beat_selection_overlay.py

            graph_editor.adjustment_panel.update_turns_panel(blue_turns, red_turns)
            graph_editor.adjustment_panel.update_adjustment_panel()

            # Set the orientations in the graph editor's orientation changer
            if isinstance(beat_view, StartPositionBeatView):
                start_pos_pictograph = beat_view.beat
                blue_start_pos_ori_picker = graph_editor.adjustment_panel.blue_start_pos_ori_picker
                red_start_pos_ori_picker = graph_editor.adjustment_panel.red_start_pos_ori_picker

                blue_start_pos_ori_picker.ori_picker_widget.set_initial_orientation(
                    start_pos_pictograph, "blue"
                )
                red_start_pos_ori_picker.ori_picker_widget.set_initial_orientation(
                    start_pos_pictograph, "red"
                )

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
