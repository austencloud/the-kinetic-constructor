from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import (
    QFont,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.beat import Beat


class BeatNumberManager:
    beat_number_text: str = "0"

    def __init__(self, beat: "Beat"):
        self.beat = beat
        self.beat_number_item: QGraphicsTextItem = None

    def add_beat_number(self, beat_number_text=None) -> None:
        if self.beat_number_item:
            self.beat_number_item.setVisible(False)
            
        self.beat_number_text = beat_number_text
        self.beat_number_item = QGraphicsTextItem(str(self.beat_number_text))
        self.beat_number_item.setFont(QFont("Georgia", 70, QFont.Weight.DemiBold))
        self.beat_number_item.setPos(
            QPointF(
                self.beat_number_item.boundingRect().height() // 3,
                self.beat_number_item.boundingRect().height() // 5,
            )
        )
        self.beat.addItem(self.beat_number_item)

    def get_beat_number_text(self) -> str:
        """
        Return the beat number or range of numbers if this beat spans multiple beats.
        """
        if self.beat.duration > 1:
            end_beat = self.beat_number_text + self.beat.duration - 1
            return f"{self.beat_number_text},{end_beat}"
        else:
            return str(self.beat_number_text)
