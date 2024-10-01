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
        self.is_placeholder = False
        self.parent_beat = None
        self.beat_number = 0  # Track the actual beat number as an integer

    def get_beat_number_text(self) -> str:
        """
        Return the beat number or range of numbers if this beat spans multiple beats.
        """
        if self.duration > 1:
            end_beat = self.beat_number + self.duration - 1
            return f"{self.beat_number},{end_beat}"
        else:
            return str(self.beat_number)


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number  # Beat number to display
        self._disable_scrollbars()
        self.beat: "Beat" = None
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

    def display_placeholder_arrow(self):
        arrow_path = get_images_and_data_path("images/placeholder_arrow.png")
        arrow_item = QGraphicsPixmapItem(QPixmap(arrow_path))
        arrow_item.setPos(
            self.sceneRect().center() - arrow_item.boundingRect().center()
        )
        self.scene().addItem(arrow_item)

    def show_context_menu(self, position):
        menu = QMenu()
        one_beat_action = QAction("1 Count", self)
        one_beat_action.triggered.connect(lambda: self.set_duration(1))
        two_beats_action = QAction("2 Counts", self)
        two_beats_action.triggered.connect(lambda: self.set_duration(2))
        menu.addAction(one_beat_action)
        menu.addAction(two_beats_action)
        menu.exec(self.mapToGlobal(position))

    def set_duration(self, duration):
        self.beat_frame.duration_manager.update_beat_duration(self, duration)

    def clear_beat(self):
        """Clear the beat from this view."""
        self.setScene(self.blank_beat)
        self.is_filled = False
        self.beat = None
        self.part_of_multibeat = False
        self.is_end = False
        self.remove_beat_number()

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

    def set_beat(self, beat: "Beat", number: int, is_end=False) -> None:
        """
        Set the beat and display its number or range.
        """
        self.beat = beat
        self.beat.view = self
        self.is_filled = True
        self.beat.beat_number = (
            number  # Store the actual beat number in the Beat object
        )
        self.is_end = is_end
        self.part_of_multibeat = self.beat.duration > 1

        # Update beat number visually
        self.setScene(self.beat)
        self.resize_beat_view()
        self.remove_beat_number()
        self.add_beat_number()

    def add_beat_number(self):
        """
        Add a beat number or a range of beat numbers to represent the beat.
        """
        # if self.beat_number_item:
        #     self.remove_beat_number()  # Remove any existing beat number item first

        # Display the beat number text (as a range if necessary)
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
