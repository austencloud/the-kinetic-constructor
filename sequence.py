from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QPushButton
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from arrow import Arrow
from artboard import Artboard
from grid import Grid
from pictograph import Pictograph
from PyQt5.QtGui import QImage, QPainter
from staff import Staff

class Sequence_Manager:
    def __init__(self, scene, pictograph_generator, main_window, info_tracker):
        self.artboard_scene = scene
        self.beats = [QGraphicsRectItem(QRectF(375, 0, 375, 375)) for i in range(4)]
        for i, section in enumerate(self.beats):
            # add a small buffer and update the x position
            section.setPos(QPointF(i * 375, 0))

        self.pictographs = [] 
        self.pictograph_generator = pictograph_generator
        self.main_window = main_window
        self.info_tracker = info_tracker

    def add_pictograph(self, pictograph):
        print("Adding pictograph")

        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.beats):
            if i >= len(self.pictographs):
                pictograph.setPos(section.pos())
                self.pictographs.append(pictograph)
                self.artboard_scene.addItem(pictograph)
                break

        print("Items in the scene:")
        for item in self.artboard_scene.items():
            print(item)

    def add_to_sequence(self, artboard):
        # Create a QImage to render the scene
        image = QImage(artboard.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)

        artboard.print_item_types()

        # deselect all items
        artboard.clear_selection()

        # Render the scene
        artboard.render(painter)
        painter.end()

        scaled_image = image.scaled(375, 375, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pictograph = Pictograph(artboard.get_state(), scaled_image)
        print(pictograph.state)
        self.add_pictograph(pictograph)
        artboard.clear()

        letter = self.info_tracker.get_current_letter()
        self.main_window.word_label.setText(self.main_window.word_label.text() + letter)

    def add_to_artboard(self, pictograph: Pictograph, artboard: Artboard):
        state = pictograph.state
        artboard.clear()
        
        for arrow_state in state['arrows']:
            arrow = Arrow(arrow_state['svg_file'])
            arrow.setPos(arrow_state['position'])
            arrow.setRotation(arrow_state['rotation'])
            arrow.color = arrow_state['color']
            arrow.quadrant = arrow_state['quadrant']
            artboard.scene().addItem(arrow)

        for staff_state in state['staffs']:
            staff = Staff(staff_state['svg_file'])
            staff.setPos(staff_state['position'])
            staff.color = staff_state['color']
            artboard.scene().addItem(staff)

        if state['grid']:
            grid = Grid(state['grid']['svg_file'])
            grid.setPos(state['grid']['position'])
            artboard.scene().addItem(grid)

    def initSequenceScene(self, layout, sequence_scene):
        self.sequence_scene = sequence_scene

        self.sequence_scene.set_manager(self)  # Set the manager of the sequence container
        self.sequence_scene.manager = self  # Set the manager of the sequence scene

        self.sequence_container = QGraphicsView(self.sequence_scene)  # Create a QGraphicsView with the sequence scene

        # Set the width and height
        self.sequence_container.setFixedSize(1700, 500)
        self.sequence_container.show()
        layout.addWidget(self.sequence_container)

    def get_clear_sequence_button(self):
        self.clear_button = QPushButton("Clear Sequence")
        self.clear_button.clicked.connect(self.clear_sequence)
        return self.clear_button

    def clear_sequence(self):
        self.pictographs = []
        for item in self.artboard_scene.items():
            self.artboard_scene.removeItem(item)
        self.main_window.word_label.setText("My word: ")

class Sequence_Scene(QGraphicsScene):
    def __init__(self, manager=None, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 4 * 375, 375)

    def set_manager(self, manager):
        self.manager = manager

