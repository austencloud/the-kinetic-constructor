from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsView, QGraphicsTextItem, QMenu, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont, QPainter, QColor, QPixmap, QImage, QAction
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class Beat(BasePictograph):
    def __init__(
        self, beat_frame: "SequenceWidgetBeatFrame", duration: Union[int, float] = 1
    ):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.view: "BeatView" = None
        self.beat_number_item: QGraphicsTextItem = None
        self.duration = duration

    def add_beat_number(self, number: int) -> None:
        if not self.beat_number_item:
            beat_text = self.get_beat_number_text(number)
            self.beat_number_item = QGraphicsTextItem(beat_text)
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
            self.beat_number_item.setPlainText(self.get_beat_number_text(number))

    def remove_beat_number(self) -> None:
        if self.beat_number_item:
            self.view.scene().removeItem(self.beat_number_item)
            self.beat_number_item = None
            self.update()

    def get_beat_number_text(self, number: int) -> str:
        if self.duration > 1:
            end_beat = number + self.duration - 1
            return f"{number}-{end_beat}"
        else:
            return str(number)


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number  # Beat number to display
        self._disable_scrollbars()
        self.beat = None
        self.beat_frame = beat_frame
        self.beat_number_item = None
        self.is_start_pos = False
        self.is_filled = False
        self.is_selected = False
        self.part_of_multibeat = False
        self.is_start = False
        self.is_end = False
        self.is_placeholder = False
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: none; border: 1px solid black;")
        self.blank_beat = Beat(self.beat_frame)
        self._setup_blank_beat()
        self.resize_beat_view()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_as_placeholder(self):
        self.is_placeholder = True
        self.part_of_multibeat = True
        self.is_start = True
        self.is_end = False
        self.is_filled = True
        self.beat = None
        self.scene().clear()
        self.display_placeholder_arrow()
        self.add_beat_number()

    def display_placeholder_arrow(self):
        arrow_item = QGraphicsPixmapItem(
            QPixmap(get_images_and_data_path("images\\placeholder_arrow.png"))
        )
        arrow_item.setPos(
            self.sceneRect().center() - arrow_item.boundingRect().center()
        )
        self.scene().addItem(arrow_item)

    def show_context_menu(self, position):
        menu = QMenu()
        one_beat_action = QAction("1 Beat", self)
        one_beat_action.triggered.connect(lambda: self.set_duration(1))
        two_beats_action = QAction("2 Beats", self)
        two_beats_action.triggered.connect(lambda: self.set_duration(2))
        menu.addAction(one_beat_action)
        menu.addAction(two_beats_action)
        menu.exec(self.mapToGlobal(position))

    def set_duration(self, duration):
        self.beat.duration = duration
        self.beat_frame.duration_manager.update_beat_numbers(self)

    def _setup_blank_beat(self):
        self.setScene(self.blank_beat)
        self.blank_beat.view = self
        self.blank_beat = self.blank_beat
        self.blank_beat.grid.hide()
        self.add_beat_number()
        self._add_start_text()

    def _disable_scrollbars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def add_beat_number(self):
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

    def remove_beat_number(self):
        self.scene().removeItem(self.beat_number_item)

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
            self.beat_frame.selection_overlay.select_beat(self)

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

    def set_beat(self, beat: "Beat", number: int, is_end=False) -> None:
        self.beat = beat
        self.is_filled = True
        self.number = number
        self.is_end = is_end
        self.part_of_multibeat = self.beat.duration > 1
        self.is_placeholder = not self.is_end and self.part_of_multibeat

        if self.is_placeholder:
            self.set_as_placeholder()
        else:
            self.setScene(self.beat)
            self.resize_beat_view()
            self.add_beat_number()
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
