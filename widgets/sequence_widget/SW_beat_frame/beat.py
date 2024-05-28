from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QPixmap,
    QImage,
)
from widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.sequence_recorder.SR_beat_frame import SR_BeatFrame
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
        SW_BeatFrame,
    )


class Beat(Pictograph):
    def __init__(self, beat_frame: Union["SW_BeatFrame", "SR_BeatFrame"]):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.view: "BeatView" = None
        self.beat_number_item: QGraphicsTextItem = None

    def add_beat_number(self, number: int) -> None:
        if not self.beat_number_item:
            self.beat_number_item = QGraphicsTextItem(str(number))
            self.beat_number_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
            self.beat_number_item.setPos(
                QPointF(
                    self.beat_number_item.boundingRect().height() // 3,
                    self.beat_number_item.boundingRect().height() // 5,
                )
            )
            if self.view and self.view.scene():
                self.view.scene().addItem(self.beat_number_item)
        else:
            self.beat_number_item.setPlainText(str(number))


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "SW_BeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number  # Beat number to display
        self._disable_scrollbars()

        self.beat_frame = beat_frame
        self.is_start_pos = False
        self.is_filled = False
        self.is_selected = False
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none; border: 1px solid black;")
        self.blank_beat = Beat(self.beat_frame)
        self._setup_blank_beat()
        self.resize_beat_view()

    def _setup_blank_beat(self):
        self.setScene(self.blank_beat)
        self.blank_beat.view = self
        self.blank_beat = self.blank_beat
        self.blank_beat.grid.hide()
        self._add_number_text()
        self._add_start_text()

    def _disable_scrollbars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _add_number_text(self):
        if self.number is not None:
            self.beat_number_item = QGraphicsTextItem(str(self.number))
            self.beat_number_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
            self.beat_number_item.setPos(
                QPointF(
                    self.beat_number_item.boundingRect().height() // 3,
                    self.beat_number_item.boundingRect().height() // 5,
                )
            )
            self.scene().addItem(self.beat_number_item)

    def _add_start_text(self):
        self.start_text_item = QGraphicsTextItem("Start")
        self.start_text_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
        text_padding = self.scene().height() // 28
        self.start_text_item.setPos(QPointF(text_padding, text_padding))
        self.scene().addItem(self.start_text_item)
        self.start_text_item.setVisible(self.is_start_pos)

    def mouseDoubleClickEvent(self, event) -> None:
        self.mousePressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.beat_frame.selection_manager.select_beat(self)

    def deselect(self) -> None:
        self.is_selected = False
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        if self.is_selected:
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

    def enterEvent(self, event):
        if self.is_filled:
            if not self.is_selected:
                self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def grab(self) -> QPixmap:
        original_size = self.sceneRect().size().toSize()
        target_width = original_size.width()
        target_height = original_size.height()
        image = QImage(target_width, target_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.scene():
            painter.setPen(QColor(0, 0, 0))
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
        self.beat.view = self

    def resize_beat_view(self):
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def clear_beat(self) -> None:
        self.is_filled = False
        self.blank_beat = None

    def set_temporary_beat(self, pictograph_dict: dict) -> None:
        self.setStyleSheet("border: 2px solid yellow;")
        self.beat.updater.update_pictograph(pictograph_dict)

    def remove_temporary_beat(self) -> None:
        self.setStyleSheet("")
        self.beat.clear()