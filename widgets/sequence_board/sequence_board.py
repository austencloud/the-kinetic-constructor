from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QImage, QPainter
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsScene, QPushButton

from settings.numerical_constants import (
    GRAPHBOARD_HEIGHT,
    GRAPHBOARD_WIDTH,
    PICTOGRAPH_SCALE,
)
from widgets.sequence_board.sequence_board_view import SequenceBoardView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graphboard.graphboard import GraphBoard

from utilities.pictograph_generator import PictographGenerator


class SequenceBoard(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graphboard = graphboard
        self.setup_view_and_controls()
        self.pictographs = []
        self.beats = []
        self.generator: "PictographGenerator" = None

        for j in range(4):
            for i in range(4):
                section = QGraphicsRectItem(
                    QRectF(
                        0,
                        0,
                        self.view.width() * 0.25,
                        self.view.height() * 0.25,
                    )
                )
                section.setPos(
                    QPointF(i * self.view.width() * 0.25, j * self.view.height() * 0.25)
                )
                self.beats.append(section)
                self.addItem(section)

        self.setSceneRect(0, 0, self.view.width(), self.view.height() * 4)

    def setup_view_and_controls(self) -> None:
        # Setup view
        self.view = SequenceBoardView(self)

        # Setup controls
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)

        # Assigning attributes to main_widget for access
        self.main_widget.sequence_board = self
        self.main_widget.sequence_view = self.view
        self.main_widget.sequence_board = self.view
        self.main_widget.clear_sequence_button = self.clear_sequence_button

    def add_to_sequence(self) -> None:
        # Get the size of the sequence_board in sequence_board coordinates
        scene_size = self.graphboard.sceneRect().size().toSize()

        # Create the QImage with the adjusted size
        image = QImage(scene_size, QImage.Format.Format_ARGB32)
        image.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(image)

        self.graphboard.clear()

        # Render the sequence_board
        self.graphboard.render(painter)
        painter.end()

        scaled_image = image.scaled(
            int(GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE),
            int(GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        state = (self.graphboard.get_state(), scaled_image)

        self.graphboard.update_letter(None)

        self.update()

    def clear_sequence(self) -> None:
        self.pictographs = []
        for item in self.items():
            self.removeItem(item)
        self.main_widget.word_label.setText("My word: ")
