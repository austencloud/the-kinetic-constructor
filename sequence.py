from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from arrow import Arrow
from artboard import Artboard
from grid import Grid
from pictograph import Pictograph
from PyQt5.QtGui import QImage, QPainter
from staff import Staff

class Sequence_Manager:
    def __init__(self, scene):
        self.scene = scene
        self.beats = [QGraphicsRectItem(QRectF(i * 375, 0, 375, 375)) for i in range(4)]
        for section in self.beats:
            self.scene.addItem(section)
            # add a small buffer
            section.setPos(section.pos() + QPointF(0, 25))

    def add_pictograph(self, pictograph):
        print("Adding pictograph")
        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.beats):
            if i >= len(self.scene.pictographs):
                # Set the position of the pictograph to the position of the section
                pictograph.setPos(section.pos())
                self.scene.pictographs.append(pictograph)
                self.scene.addItem(pictograph)
                break
        print("Items in the scene:")
        for item in self.scene.items():
            print(item)

    def add_to_sequence(self, artboard):
        # Create a QImage to render the scene
        image = QImage(artboard.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        artboard.render(painter)
        painter.end()
        scaled_image = image.scaled(375, 375, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pictograph = Pictograph(artboard.get_state(), scaled_image)
        print(pictograph.state)
        pictograph.setFlag(QGraphicsItem.ItemHasNoContents)
        self.add_pictograph(pictograph)

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
            
        self.sequence_scene.remove_pictograph(pictograph)


class Sequence_Scene(QGraphicsScene):
    def __init__(self, manager=None, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.pictographs = []
    
    def set_manager(self, manager):
        self.manager = manager