from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_pictograph import GE_BlankPictograph


class GE_PictographView(PictographView):
    def __init__(
        self, GE: "GraphEditor", blank_pictograph: "GE_BlankPictograph"
    ) -> None:
        super().__init__(blank_pictograph)
        self.GE = GE
        self.is_start_pos = False
        self.blank_pictograph = blank_pictograph
        self.main_widget = GE.main_widget
        self.setScene(blank_pictograph)
        self.setFrameShape(PictographView.Shape.Box)

    def resize_GE_pictograph_view(self):
        self.setMinimumHeight(self.GE.height())
        self.setMinimumWidth(self.GE.height())

        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_to_blank_grid(self):
        self.setScene(self.blank_pictograph)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())  # Use the viewport to draw over the content
        pen = QPen(Qt.GlobalColor.black, 0)  # Set the color and width of the border
        painter.setPen(pen)

        right_edge = self.viewport().width() - 1
        painter.drawLine(right_edge, 0, right_edge, self.viewport().height())
        overlay_color = QColor("gold")
        overlay_pen = QPen(overlay_color, 4)
        overlay_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(overlay_pen)

        overlay_rect = self.viewport().rect().adjusted(
            overlay_pen.width() // 2,
            overlay_pen.width() // 2,
            -overlay_pen.width() // 2,
            -overlay_pen.width() // 2,
        )
        painter.drawRect(overlay_rect)

    def get_current_pictograph(self) -> Pictograph:
        return self.scene() 
    
    def set_scene(self, beat_view: "BeatView"):
        self.setScene(beat_view)
        if beat_view.is_start_pos:
            self.is_start_pos = True
        


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
            graph_editor.turns_panel.update_turns_panel(blue_turns, red_turns)
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


class GE_BlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)
