from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_board.sequence_board import SequenceBoard


class SequenceBoardView(QGraphicsView):
    def __init__(self, sequence_board: "SequenceBoard") -> None:
        super().__init__(sequence_board)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedSize(
            int(sequence_board.graphboard.view.width() * 2.5),
            int(sequence_board.graphboard.view.height() * 2.5),
        )
