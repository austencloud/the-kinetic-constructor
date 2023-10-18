from PyQt6.QtWidgets import QGraphicsRectItem, QPushButton
from PyQt6.QtCore import QRectF, Qt, QPointF,  QObject
from PyQt6.QtGui import QImage, QPainter, QColor
from objects.arrow import Arrow
from objects.staff import Staff
from objects.grid import Grid
from views.graphboard_view import Graphboard_View
from pictograph import Pictograph
from settings import DEFAULT_GRAPHBOARD_WIDTH, DEFAULT_GRAPHBOARD_HEIGHT, PICTOGRAPH_SCALE

class Sequence_Manager(QObject):
    def __init__(self, sequence_scene, pictograph_generator, main_widget, info_tracker):
        self.pictographs = [] 
        self.pictograph_generator = pictograph_generator
        self.main_widget = main_widget   
        self.info_tracker = info_tracker
        self.sequence_scene = sequence_scene
        self.beats = [QGraphicsRectItem(QRectF(0, 0, DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE, DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE)) for i in range(4)]
        
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

        scaled_image = image.scaled(int(DEFAULT_GRAPHBOARD_WIDTH * PICTOGRAPH_SCALE), int(DEFAULT_GRAPHBOARD_HEIGHT * PICTOGRAPH_SCALE), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pictograph = Pictograph(graphboard.get_graphboard_state(), scaled_image)
        self.add_pictograph(pictograph)
        graphboard.clear()
        graphboard.update_letter(None)
        letter = self.info_tracker.get_current_letter()
        if letter:
            self.main_widget.word_label.setText(self.main_widget.word_label.text() + letter)
        self.sequence_scene.update()


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
        for item in self.sequence_scene.items():
            self.sequence_scene.removeItem(item)
        self.main_widget.word_label.setText("My word: ")
        self.main_widget.info_tracker.label.setText("")  # Clear the label
        

