from typing import TYPE_CHECKING

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget

from utilities.TypeChecking.TypeChecking import LetterDictionary
from utilities.export_handler import ExportHandler
from utilities.json_handler import JsonHandler
from utilities.layout_manager import LayoutManager
from utilities.pictograph_generator import PictographGenerator
from widgets.graph_editor.key_event_handler import KeyEventHandler
from widgets.graph_editor.graph_editor import GraphEditor
from widgets.option_picker.option_picker import OptionPicker
from widgets.sequence.sequence import Sequence

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window
        self.resize(int(self.main_window.width()), int(self.main_window.height()))

        self.key_event_handler = KeyEventHandler()
        self.json_handler = JsonHandler()
        self.letters: LetterDictionary = self.json_handler.load_all_letters()

        self.graph_editor = GraphEditor(self)
        self.option_picker = OptionPicker(self)
        self.sequence = Sequence(self)

        self.generator = PictographGenerator(self)
        self.export_handler = ExportHandler(self)
        self.layout_manager = LayoutManager(self)
        self.layout_manager.configure_layouts()

    ### EVENTS ###

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            self.key_event_handler.keyPressEvent(
                event, self, self.graph_editor.pictograph
            )
            return True
        return super().eventFilter(source, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize(int(self.main_window.width()), int(self.main_window.height()))

        self.sequence.update_size()
        self.option_picker.update_size()
        self.graph_editor.update_size()
