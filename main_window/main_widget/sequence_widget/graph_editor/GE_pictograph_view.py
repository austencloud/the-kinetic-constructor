from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor

from base_widgets.base_pictograph.components.pictograph_view import (
    PictographView,
)
from base_widgets.base_pictograph.base_pictograph import BasePictograph


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
        GraphEditorPictographContainer,
    )
    from main_window.main_widget.sequence_widget.beat_frame.beat_view import (
        Beat,
    )

    from .GE_pictograph_view import GE_BlankPictograph


class GE_PictographView(PictographView):
    def __init__(
        self,
        pictograph_container: "GraphEditorPictographContainer",
        blank_pictograph: "GE_BlankPictograph",
    ) -> None:
        super().__init__(blank_pictograph)
        self.graph_editor = pictograph_container.graph_editor
        self.is_start_pos = False
        self.blank_pictograph = blank_pictograph
        self.main_widget = self.graph_editor.main_widget
        self.setScene(blank_pictograph)
        self.setFrameShape(PictographView.Shape.Box)

    def set_to_blank_grid(self) -> None:
        self.blank_pictograph = GE_BlankPictograph(self)
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

    def get_current_pictograph(self) -> BasePictograph:
        return self.scene()

    def set_scene(self, beat: "Beat") -> None:
        self.setScene(beat)
        self.pictograph = beat
        if beat.view.is_start_pos:
            self.is_start_pos = True
        else:
            self.is_start_pos = False
        self.repaint()

    def resizeEvent(self, event) -> None:
        # self.setFixedSize(self.graph_editor.height(), self.graph_editor.height())

        scene_size = self.scene().sceneRect().size()
        view_size = self.viewport().size()
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )
        self.resetTransform()
        self.scale(scale_factor, scale_factor)


class GE_BlankPictograph(BasePictograph):
    def __init__(self, pictograph_container: "GraphEditorPictographContainer") -> None:
        super().__init__(pictograph_container.graph_editor.main_widget)
        self.is_blank = True
