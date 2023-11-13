from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsRectItem, QPushButton
from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QImage, QPainter, QColor
from objects.arrow import Arrow
from objects.staff import Staff
from objects.grid import Grid
from widgets.graph_editor.graphboard.graphboard import Graphboard
from settings.numerical_constants import *
from settings.string_constants import *


class SequenceView(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        sequence_scene = QGraphicsScene()

        sequence_scene.setSceneRect(0, 0, SEQUENCE_SCENE_WIDTH, SEQUENCE_SCENE_HEIGHT)

        self.setFixedSize(
            int(sequence_scene.sceneRect().width()),
            int(sequence_scene.sceneRect().height()),
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.show()

        clear_sequence_button = QPushButton("Clear Sequence")
        clear_sequence_button.clicked.connect(self.clear_sequence)

        main_widget.word_label = QLabel(main_widget.main_window)

        main_widget.word_label.setFont(QFont("Helvetica", 20))
        main_widget.word_label.setText("My word: ")

        main_widget.sequence_scene = sequence_scene
        main_widget.sequence_view = self
        main_widget.clear_sequence_button = clear_sequence_button

        self.pictographs = []
        self.sequence_scene = sequence_scene
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

    def add_pictograph(self, pictograph):
        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.beats):
            if i >= len(self.pictographs):
                pictograph.setPos(section.pos())
                self.pictographs.append(pictograph)
                self.sequence_scene.addItem(pictograph)
                break

    def add_to_sequence(self, graphboard):
        # Get the size of the sequence_scene in sequence_scene coordinates
        scene_size = graphboard.sceneRect().size().toSize()

        # Create the QImage with the adjusted size
        image = QImage(scene_size, QImage.Format.Format_ARGB32)
        image.fill(QColor(Qt.GlobalColor.transparent))
        painter = QPainter(image)

        graphboard.clear()

        # Render the sequence_scene
        graphboard.render(painter)
        painter.end()

        scaled_image = image.scaled(
            int(GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE),
            int(GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        state = (graphboard.get_state(), scaled_image)
        self.add_pictograph(state)

        graphboard.update_letter(None)

        self.sequence_scene.update()

    def clear_sequence(self):
        self.pictographs = []
        for item in self.sequence_scene.items():
            self.sequence_scene.removeItem(item)
        self.main_widget.word_label.setText("My word: ")
        self.main_widget.infobox.label.setText("")  # Clear the label
