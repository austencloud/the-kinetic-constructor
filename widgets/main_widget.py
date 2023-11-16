from typing import TYPE_CHECKING

from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QGraphicsView, QLabel, QPushButton, QWidget

from utilities.export_handler import ExportHandler
from utilities.json_handler import JsonHandler
from utilities.layout_manager import LayoutManager
from utilities.pictograph_generator import PictographGenerator
from widgets.events.key_event_handler import KeyEventHandler
from widgets.graph_editor import GraphEditor
from widgets.optionboard.letter_buttons_frame import LetterButtonsFrame
from widgets.optionboard.optionboard import OptionBoard
from widgets.sequence_board.sequence_board import SequenceBoard

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.propbox.propbox import PropBox

from utilities.TypeChecking.TypeChecking import LetterDictionary


class MainWidget(QWidget):
    propbox: "PropBox"
    main_window: "MainWindow"
    clear_sequence_button: "QPushButton"
    word_label: "QLabel"
    sequence_view: "QGraphicsView"

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window

        self.layout_manager = LayoutManager(self)
        self.json_handler = JsonHandler()
        self.letters: LetterDictionary = self.json_handler.load_all_letters()
        self.key_event_handler = KeyEventHandler()
        self.graph_editor = GraphEditor(self)
        self.optionboard = OptionBoard(self)
        self.letter_buttons_frame = LetterButtonsFrame(self)

        self.graphboard = self.graph_editor.graphboard
        self.infobox = self.graph_editor.infobox
        self.propbox = self.graph_editor.propbox
        self.arrowbox = self.graph_editor.arrowbox

        self.sequence_board = SequenceBoard(self, self.graphboard)
        self.generator = PictographGenerator(self, self.graphboard, self.infobox)
        self.export_handler = ExportHandler(self.graphboard)

        self.graphboard.generator = self.generator
        self.sequence_board.generator = self.generator

        self.layout_manager.configure_layouts()

    ### EVENTS ###

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            self.key_event_handler.keyPressEvent(event, self, self.graphboard)
            return True
        return super().eventFilter(source, event)
