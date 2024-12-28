from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QPixmap,
    QImage,
)
from base_widgets.base_pictograph.pictograph_view import PictographView
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatView(PictographView):
    is_start_pos = False
    is_filled = False
    is_selected = False
    is_start = False
    is_placeholder = False
    beat_number_item: QGraphicsTextItem
    beat: "Beat" = None
    
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number
        self.beat_frame = beat_frame
        self.setStyleSheet("border: none; border: 1px solid black;")
        self._setup_blank_beat()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_blank_beat(self):
        self.blank_beat = StartPositionBeat(self.beat_frame)
        self.setScene(self.blank_beat)
        self.blank_beat.grid.hide()
        self.add_beat_number()

    def set_beat(self, beat: "Beat", number: int) -> None:
        self.beat = beat
        self.beat.view = self
        self.is_filled = True
        self.beat.beat_number = number
        self.setScene(self.beat)
        self.remove_beat_number()
        self.add_beat_number()
        self.beat.reversal_symbol_manager.update_reversal_symbols()

    def add_beat_number(self, beat_number_text=None) -> None:
        if not beat_number_text:
            beat_number_text = (
                self.beat.get_beat_number_text()
                if self.beat
                else self.blank_beat.get_beat_number_text()
            )

        self.beat_number_item = QGraphicsTextItem(beat_number_text)
        self.beat_number_item.setFont(QFont("Georgia", 80, QFont.Weight.DemiBold))
        self.beat_number_item.setPos(
            QPointF(
                self.beat_number_item.boundingRect().height() // 3,
                self.beat_number_item.boundingRect().height() // 5,
            )
        )
        self.scene().addItem(self.beat_number_item)

    def remove_beat_number(self):
        if self.beat_number_item:
            self.beat_number_item.setVisible(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.beat_frame.selection_overlay.select_beat(self)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
