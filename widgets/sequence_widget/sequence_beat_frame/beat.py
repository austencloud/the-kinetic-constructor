from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QPushButton, QGraphicsTextItem
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QIcon, QMouseEvent, QFont, QPaintEvent, QPainter, QColor
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.view: "BeatView" = None


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number  # Beat number to display
        self._disable_scrollbars()
        self.beat_frame = beat_frame
        self.selection_manager = self.beat_frame.selection_manager
        self.beat: "Beat" = None
        self.is_start_pos = False
        self.is_filled = False
        self.is_selected = False
        self.setContentsMargins(0, 0, 0, 0)

    def _disable_scrollbars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_pictograph(self, new_beat: "Beat") -> None:
        self.beat = new_beat
        new_beat.view = self
        new_beat.view.is_filled = True
        self.setScene(self.beat)
        view_width = self.height()
        self.view_scale = view_width / self.beat.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def clear(self):
        self.setScene(None)
        self.beat_frame.start_pos_view.setScene(None)
        sequence_builder = self.beat.main_widget.builder_toolbar.sequence_builder
        sequence_builder.current_pictograph = self.beat_frame.start_pos
        sequence_builder.reset_to_start_pos_picker()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.mousePressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.selection_manager.select_beat(self)

    def deselect(self) -> None:
        self.is_selected = False
        self.update()

    # in the paint event, place the number at the top left of the beat view using QPainter
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        if self.number is not None:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(0, 0, 0))
            painter.setFont(QFont("Georgia", 20, QFont.Weight.Bold))
            painter.drawText(QRect(0, 0, 50, 50), Qt.AlignmentFlag.AlignLeft, str(self.number))
            painter.end()
        if self.is_selected:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
            painter.end()