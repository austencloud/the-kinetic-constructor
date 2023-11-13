from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QLabel, QPushButton, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QPointF, Qt
from PyQt6.QtGui import QFont, QImage, QPainter, QColor
from settings.numerical_constants import (
    SEQUENCE_SCENE_HEIGHT,
    SEQUENCE_SCENE_WIDTH,
    GRAPHBOARD_HEIGHT,
    GRAPHBOARD_WIDTH,
    PICTOGRAPH_SCALE,
)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from utilities.pictograph_generator import PictographGenerator
    from widgets.graphboard.graphboard import Graphboard

class SequenceScene(QGraphicsScene):
    generator: 'PictographGenerator'
    graphboard: 'Graphboard'
    
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()

        self.setSceneRect(0, 0, SEQUENCE_SCENE_WIDTH, SEQUENCE_SCENE_HEIGHT)
        self.main_widget = main_widget
        self.pictographs = []
        self.beats = [
            QGraphicsRectItem(
                QRectF(
                    0,
                    0,
                    GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE,
                    GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE,
                )
            )
            for i in range(4)
        ]

        for i, section in enumerate(self.beats):
            section.setPos(QPointF(i * GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE, 0))
            self.addItem(section)

        self.setup_view_and_controls()

    def setup_view_and_controls(self):
        # Setup view
        self.view = QGraphicsView(self)
        self.view.setFixedSize(
            int(self.sceneRect().width()),
            int(self.sceneRect().height()),
        )
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Setup controls
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)

        self.word_label = QLabel(self.main_widget.main_window)
        self.word_label.setFont(QFont("Helvetica", 20))
        self.word_label.setText("My word: ")

        # Assigning attributes to main_widget for access
        self.main_widget.sequence_scene = self
        self.main_widget.sequence_view = self.view
        self.main_widget.sequence_scene = self.view
        self.main_widget.clear_sequence_button = self.clear_sequence_button
        self.main_widget.word_label = self.word_label

    # Rest of the methods remain the same

    def add_to_sequence(self):
        # Get the size of the sequence_scene in sequence_scene coordinates
        scene_size = self.graphboard.sceneRect().size().toSize()

        # Create the QImage with the adjusted size
        image = QImage(scene_size, QImage.Format.Format_ARGB32)
        image.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(image)

        self.graphboard.clear()

        # Render the sequence_scene
        self.graphboard.render(painter)
        painter.end()

        scaled_image = image.scaled(
            int(GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE),
            int(GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        state = (self.graphboard.get_state(), scaled_image)
        self.add_pictograph(state)

        self.graphboard.update_letter(None)

        self.update()

    def clear_sequence(self):
        self.pictographs = []
        for item in self.items():
            self.removeItem(item)
        self.main_widget.word_label.setText("My word: ")

