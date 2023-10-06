from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QPushButton
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from arrow import Arrow
from graphboard import Graphboard_View
from grid import Grid
from pictograph import Pictograph
from PyQt5.QtGui import QImage, QPainter
from staff import Staff
from settings import Settings
from graphboard import Graphboard_View

SCALE_FACTOR = Settings.SCALE_FACTOR
class Sequence_Manager():
    def __init__(self, scene, pictograph_generator, ui_setup, info_tracker):
        self.graphboard_scene = scene
        self.beats = [QGraphicsRectItem(QRectF(int(375 * SCALE_FACTOR), 0, int(375 * SCALE_FACTOR), int(375 * SCALE_FACTOR))) for i in range(4)]
        for i, section in enumerate(self.beats):

            section.setPos(QPointF(i * int(375 * SCALE_FACTOR), 0))

        self.pictographs = [] 
        self.pictograph_generator = pictograph_generator
        self.ui_setup = ui_setup
        self.info_tracker = info_tracker

    def add_pictograph(self, pictograph):
        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.beats):
            if i >= len(self.pictographs):
                pictograph.setPos(section.pos())
                self.pictographs.append(pictograph)
                self.graphboard_scene.addItem(pictograph)
                break

    def add_to_sequence(self, graphboard):
        # Get the size of the scene in scene coordinates
        scene_size = graphboard.sceneRect().size().toSize()

        # Add the height of the letter (assuming it's 200 pixels tall, adjust as necessary)
        scene_size.setHeight(scene_size.height() + int(200 * SCALE_FACTOR))

        # Create the QImage with the adjusted size
        image = QImage(scene_size, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)

        # deselect all items
        graphboard.clear_selection()

        # Render the scene
        graphboard.render(painter)
        painter.end()


        scaled_image = image.scaled(int(375 * SCALE_FACTOR), int(375 * SCALE_FACTOR), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pictograph = Pictograph(graphboard.get_state(), scaled_image)
        print(pictograph.state)
        self.add_pictograph(pictograph)
        graphboard.clear()
        graphboard.update_letter(None)
        letter = self.info_tracker.get_current_letter()
        self.ui_setup.word_label.setText(self.ui_setup.word_label.text() + letter)
  

    def add_to_graphboard(self, pictograph: Pictograph, graphboard_view: Graphboard_View):
        state = pictograph.state
        graphboard_view.clear()

        
        for arrow_state in state['arrows']:
            arrow = Arrow(arrow_state['svg_file'])
            arrow.setPos(arrow_state['position'])
            arrow.setRotation(arrow_state['rotation'])
            arrow.color = arrow_state['color']
            arrow.quadrant = arrow_state['quadrant']
            graphboard_view.scene().addItem(arrow)

        for staff_state in state['staffs']:
            staff = Staff(staff_state['svg_file'])
            staff.setPos(staff_state['position'])
            staff.color = staff_state['color']
            graphboard_view.scene().addItem(staff)

        if state['grid']:
            grid = Grid(state['grid']['svg_file'])
            grid.setPos(state['grid']['position'])
            graphboard_view.scene().addItem(grid)

    def get_clear_sequence_button(self):
        self.clear_button = QPushButton("Clear Sequence")
        self.clear_button.clicked.connect(self.clear_sequence)
        return self.clear_button

    def clear_sequence(self):
        self.pictographs = []
        for item in self.graphboard_scene.items():
            self.graphboard_scene.removeItem(item)
        self.ui_setup.word_label.setText("My word: ")
        self.ui_setup.info_tracker.label.setText("")  # Clear the label


class Sequence_Scene(QGraphicsScene):
    def __init__(self, manager=None, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 4 * 375, 375)

    def set_manager(self, manager):
        self.manager = manager

