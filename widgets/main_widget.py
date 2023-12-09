from typing import TYPE_CHECKING, Optional

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
from widgets.graph_editor.pictograph.pictograph import Pictograph
from widgets.option_picker.option_picker_widget import OptionPickerWidget
from widgets.sequence.sequence_widget import SequenceWidget

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
        self.option_picker = OptionPickerWidget(self)
        self.sequence = SequenceWidget(self)

        self.generator = PictographGenerator(self)
        self.export_handler = ExportHandler(self)
        self.layout_manager = LayoutManager(self)
        self.layout_manager.configure_layouts()

    ### EVENTS ###

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            active_pictograph = self.find_active_pictograph()
            if active_pictograph:
                self.key_event_handler.keyPressEvent(event, self, active_pictograph)
                return True
        return super().eventFilter(source, event)

    def deselect_all_except(self, active_pictograph: Pictograph) -> None:
        if self.graph_editor.pictograph != active_pictograph:
            self.graph_editor.pictograph.clearSelection()

        for beat_view in self.sequence.frame.beats:
            if beat_view.pictograph and beat_view.pictograph != active_pictograph:
                beat_view.pictograph.clearSelection()

    def find_active_pictograph(self) -> Optional[Pictograph]:
        # Check if the main pictograph has a selected item
        if self.graph_editor.pictograph.selectedItems():
            return self.graph_editor.pictograph

        # Check each beat for a selected item
        for beat_view in self.sequence.frame.beats:
            if beat_view.pictograph and beat_view.pictograph.selectedItems():
                return beat_view.pictograph

        return None

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass
        self.sequence.update_size()
        self.option_picker.update_size()
        self.graph_editor.update_size()