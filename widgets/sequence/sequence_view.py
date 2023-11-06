from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsRectItem, QPushButton
from PyQt6.QtCore import QRectF, Qt, QPointF
from PyQt6.QtGui import QImage, QPainter, QColor
from objects.arrow.arrow import Arrow
from objects.staff.staff import Staff
from objects.grid import Grid
from widgets.graph_editor.graphboard.graphboard import Graphboard
from objects.pictograph.pictograph_image import PictographImage
from config.numerical_constants import (
    DEFAULT_GRAPHBOARD_WIDTH,
    DEFAULT_GRAPHBOARD_HEIGHT,
    PICTOGRAPH_SCALE,
    GRAPHBOARD_VIEW_HEIGHT,
)
from config.string_constants import *


class SequenceView(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        sequence_scene = QGraphicsScene()

        sequence_scene.setSceneRect(
            0, 0, GRAPHBOARD_VIEW_HEIGHT * 2, GRAPHBOARD_VIEW_HEIGHT * 2
        )

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
                    DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE,
                    DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE,
                )
            )
            for i in range(4)
        ]

        for i, section in enumerate(self.beats):
            section.setPos(QPointF(i * DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE, 0))

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

        graphboard.clear_selection()

        # Render the sequence_scene
        graphboard.render(painter)
        painter.end()

        scaled_image = image.scaled(
            int(DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE),
            int(DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        pictograph = PictographImage(graphboard.get_state(), scaled_image)
        self.add_pictograph(pictograph)
        graphboard.clear_graphboard()
        graphboard.update_letter(None)
        letter = self.info_handler.determine_current_letter_and_type()[0]
        if letter:
            self.main_widget.word_label.setText(
                self.main_widget.word_label.text() + letter
            )
        self.sequence_scene.update()

    def add_to_graphboard(self, pictograph: PictographImage, graphboard: Graphboard):
        state = pictograph.state
        graphboard.clear_graphboard()

        for arrow_state in state[ARROWS]:
            arrow = Arrow(arrow_state["svg_file"])
            arrow.setPos(arrow_state["position"])
            arrow.setRotation(arrow_state["rotation"])
            arrow.color = arrow_state[COLOR]
            arrow.quadrant = arrow_state[QUADRANT]
            graphboard.scene().addItem(arrow)

        for staff_state in state["staffs"]:
            staff = Staff(staff_state["svg_file"])
            staff.setPos(staff_state["position"])
            staff.color = staff_state[COLOR]
            graphboard.scene().addItem(staff)

        if state["grid"]:
            grid = Grid(state["grid"]["svg_file"])
            grid.setPos(state["grid"]["position"])
            graphboard.scene().addItem(grid)

    def clear_sequence(self):
        self.pictographs = []
        for item in self.sequence_scene.items():
            self.sequence_scene.removeItem(item)
        self.main_widget.word_label.setText("My word: ")
        self.main_widget.infobox.label.setText("")  # Clear the label
