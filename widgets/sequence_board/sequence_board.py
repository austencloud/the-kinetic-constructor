from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QImage, QPainter
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGridLayout,
    QPushButton,
    QGraphicsView,
    QFrame,
)

from settings.numerical_constants import (
    GRAPHBOARD_HEIGHT,
    GRAPHBOARD_WIDTH,
    PICTOGRAPH_SCALE,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graphboard.graphboard import GraphBoard

from utilities.pictograph_generator import PictographGenerator
from PyQt6.QtWidgets import QSizePolicy


class SequenceBoard(QFrame):
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graphboard = graphboard
        self.setup_view_and_controls()
        self.pictographs = []
        self.beats = []

        self.generator: "PictographGenerator" = None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a QGridLayout for the QFrame
        self.layout = QGridLayout(self)

        for j in range(4):
            for i in range(4):
                view = QGraphicsView()
                scene = QGraphicsScene()

                view.setScene(scene)

                view.setSceneRect(0, 0, 100, 100)

                rect = QRectF(0, 0, 50, 50)
                color = QColor(255, 0, 0)
                scene.addRect(rect, color)

                self.layout.addWidget(view, j, i)

                self.beats.append(view)

    def setup_view_and_controls(self) -> None:
        self.clear_sequence_button = QPushButton("Clear Sequence")
        # set the height of the button
        self.clear_sequence_button.setFixedHeight(50)
        self.clear_sequence_button.clicked.connect(self.clear_sequence)

        self.main_widget.sequence_board = self
        self.main_widget.clear_sequence_button = self.clear_sequence_button

    def add_to_sequence(self) -> None:
        scene_size = self.graphboard.sceneRect().size().toSize()

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
