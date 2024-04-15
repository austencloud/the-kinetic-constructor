from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRect, QPointF
from PyQt6.QtGui import (
    QMouseEvent,
    QFont,
    QPaintEvent,
    QPainter,
    QColor,
    QPixmap,
    QImage,
    QPen,
)
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.sequence_recorder.SR_beat_frame import SR_BeatFrame
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
        SW_Beat_Frame,
    )


class Beat(Pictograph):
    def __init__(self, beat_frame: Union["SW_Beat_Frame", "SR_BeatFrame"]):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.view: "BeatView" = None

    def add_beat_number(self, number: int) -> None:
        beat_number_item = QGraphicsTextItem(str(number))
        beat_number_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
        beat_number_item.setPos(
            QPointF(
                beat_number_item.boundingRect().height() // 3,
                beat_number_item.boundingRect().height() // 5,
            )
        )
        if self.view and self.view.scene():
            self.view.scene().addItem(beat_number_item)


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "SW_Beat_Frame", number=None):
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
        # add a 2px black border
        self.setStyleSheet("border: none; border: 1px solid black;")

    def _disable_scrollbars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
            painter.drawText(
                QRect(0, 0, 50, 50), Qt.AlignmentFlag.AlignLeft, str(self.number)
            )
            painter.end()
        if self.is_selected:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
            painter.end()

    def enterEvent(self, event):
        if self.scene() is not None:
            # if it's not currently selected
            if not self.is_selected:
                self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def grab(self) -> QPixmap:
        # Calculate the required size
        original_size = self.sceneRect().size().toSize()
        target_width = original_size.width()
        target_height = original_size.height()

        # Create a QImage with the specified size and render the scene onto it
        image = QImage(target_width, target_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)  # Fill with transparent background

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # For smooth edges

        if not self.scene():

            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setBrush(QColor(0, 255, 255))
            painter.drawRect(0, 0, target_width - 1, target_height - 1)
        else:
            self.scene().render(painter)

        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(0, 0, target_width - 1, target_height - 1)

        painter.end()

        return QPixmap.fromImage(image)

    def set_beat(self, start_pos: "Beat", number: int) -> None:
        self.start_pos = self.beat = start_pos
        self.is_filled = True
        self.start_pos.view = self
        self.setScene(self.start_pos)
        self.resize_beat_view()
        self.beat.add_beat_number(number)

    def resize_beat_view(self):
        self.view_scale = (
            self.height() / self.start_pos.width()
            if self.start_pos
            else self.beat.width()
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        print(
            f"View Height: - {self.height()}, Scene height - {self.start_pos.height() if self.start_pos else 'None'}"
        )
