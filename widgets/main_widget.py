from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import QEvent
from utilities.json_handler import JsonHandler
from widgets.sequence.sequence_scene import SequenceScene
from widgets.optionboard.optionboard_view import OptionboardView
from utilities.layout_manager import LayoutManager
from widgets.events.key_event_handler import KeyEventHandler
from widgets.graph_editor import GraphEditor
from widgets.optionboard.letter_buttons_frame import LetterButtonsFrame
from utilities.pictograph_generator import PictographGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.propbox.propbox import Propbox


class MainWidget(QWidget):
    propbox: "Propbox"
    main_window: "MainWindow"
    clear_sequence_button: "QPushButton"
    word_label: "QLabel"
    sequence_view: "QGraphicsView"

    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window

        self.sequence_scene = SequenceScene(self)
        self.layout_manager = LayoutManager(self)
        self.json_handler = JsonHandler()
        self.letters = self.json_handler.load_all_letters()
        self.key_event_handler = KeyEventHandler()

        self.graph_editor = GraphEditor(self)
        self.optionboard_view = OptionboardView(self)
        self.letter_buttons_frame = LetterButtonsFrame(self)

        self.graphboard = self.graph_editor.graphboard
        self.sequence_scene.graphboard = self.graphboard
        self.infobox = self.graph_editor.infobox
        self.propbox = self.graph_editor.propbox
        self.arrowbox = self.graph_editor.arrowbox

        self.generator = PictographGenerator(self, self.graphboard, self.infobox)
        self.graphboard.generator = self.generator
        self.sequence_scene.generator = self.generator

        self.layout_manager.configure_layouts()

    ### EVENTS ###

    def eventFilter(self, source, event: QEvent):
        if event.type() == QEvent.Type.KeyPress:
            self.key_event_handler.keyPressEvent(event, self, self.graphboard)
            return True
        return super().eventFilter(source, event)
