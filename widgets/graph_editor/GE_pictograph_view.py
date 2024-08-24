from typing import TYPE_CHECKING
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor

from widgets.sequence_widget.SW_beat_frame.beat import Beat

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


if TYPE_CHECKING:
    from .GE_pictograph_view import GE_BlankPictograph


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

    def set_to_blank_grid(self) -> None:
        self.setScene(self.blank_pictograph)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        pen = QPen(Qt.GlobalColor.black, 0)
        painter.setPen(pen)

        right_edge = self.viewport().width() - 1
        painter.drawLine(right_edge, 0, right_edge, self.viewport().height())
        overlay_color = QColor("gold")
        overlay_pen = QPen(overlay_color, 4)
        overlay_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(overlay_pen)

        overlay_rect = (
            self.viewport()
            .rect()
            .adjusted(
                overlay_pen.width() // 2,
                overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
                -overlay_pen.width() // 2,
            )
        )
        painter.drawRect(overlay_rect)

    def get_current_pictograph(self) -> Pictograph:
        return self.scene()

    def set_scene(self, beat: "Beat") -> None:
        self.setScene(beat)
        self.pictograph = beat
        if beat.view.is_start_pos:
            self.is_start_pos = True
        else:
            self.is_start_pos = False

    def resize_GE_pictograph_view(self) -> None:
        self.setFixedSize(
            self.GE.height(), self.GE.height()
        )

        scene_size = self.scene().sceneRect().size()
        view_size = self.viewport().size()
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )
        self.resetTransform()
        self.scale(scale_factor, scale_factor)


class GE_BlankPictograph(Pictograph):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor.main_widget)
        self.is_blank = True
