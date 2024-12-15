from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QMouseEvent, QKeyEvent, QCursor
from PyQt6.QtWidgets import QApplication

from base_widgets.base_pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)
from base_widgets.base_pictograph.pictograph_view import (
    PictographView,
)
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.pictograph_view_key_event_handler import (
    PictographViewKeyEventHandler,
)
from main_window.main_widget.sequence_widget.graph_editor.GE_pictograph_view_mouse_event_handler import (
    GE_PictographViewMouseEventHandler,
)


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
        container: "GraphEditorPictographContainer",
        blank_pictograph: "GE_BlankPictograph",
    ) -> None:
        super().__init__(blank_pictograph)
        self.graph_editor = container.graph_editor
        self.is_start_pos = False
        self.blank_pictograph = blank_pictograph
        self.main_widget = self.graph_editor.main_widget
        self.setScene(blank_pictograph)
        self.setFrameShape(PictographView.Shape.Box)
        self.mouse_event_handler = GE_PictographViewMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.key_event_handler = PictographViewKeyEventHandler(self)

    def set_to_blank_grid(self) -> None:
        self.blank_pictograph = GE_BlankPictograph(self)
        self.setScene(self.blank_pictograph)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.key_event_handler.handle_key_press(event):
            super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_event_handler.handle_mouse_press(event)
        QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        from main_window.main_widget.sequence_widget.graph_editor.pictograph_container.GE_pictograph_container import (
            GraphEditorPictographContainer,
        )

        if isinstance(self.parent(), GraphEditorPictographContainer):
            if self.mouse_event_handler.is_arrow_under_cursor(event):
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

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
