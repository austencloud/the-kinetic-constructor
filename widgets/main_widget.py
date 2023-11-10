from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QEvent
from utilities.json_handler import JsonHandler
from widgets.sequence.sequence_view import SequenceView
from widgets.optionboard.optionboard_view import OptionboardView
from utilities.layout_manager import LayoutManager
from widgets.graph_editor.events.key_event_handler import KeyEventHandler
from widgets.graph_editor.graph_editor import GraphEditor
from widgets.optionboard.letter_buttons_frame import LetterButtonsFrame
from utilities.pictograph_generator import PictographGenerator


class MainWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window

        self.layout_manager = LayoutManager(self)
        self.json_handler = JsonHandler()
        self.letters = self.json_handler.load_all_letters()
        self.key_event_handler = KeyEventHandler()

        self.sequence_view = SequenceView(self)
        self.graph_editor = GraphEditor(self)
        self.optionboard_view = OptionboardView(self)
        self.letter_buttons_frame = LetterButtonsFrame(self)

        self.graphboard = self.graph_editor.graphboard
        self.infobox = self.graph_editor.infobox
        self.propbox = self.graph_editor.propbox
        self.arrowbox = self.graph_editor.arrowbox

        self.pictograph_generator = PictographGenerator(
            self, self.graphboard, self.infobox
        )

        self.layout_manager.settingsure_layouts()
        self.connect_objects()

    def connect_objects(self):
        self.graphboard.infobox = self.graph_editor.infobox
        self.graphboard.generator = self.pictograph_generator
        self.graph_editor.graphboard.context_menu_manager.sequence_view = (
            self.sequence_view
        )
        self.sequence_view.pictograph_generator = self.pictograph_generator

    ### EVENTS ###

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            self.key_event_handler.keyPressEvent(
                event, self, self.graphboard, self.graphboard.manipulators
            )
            return True
        return super().eventFilter(source, event)
