from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from utilities.TypeChecking.TypeChecking import LetterDictionary
from utilities.export_handler import ExportHandler
from utilities.json_handler import JsonHandler
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
        self.configure_layouts()

    def configure_layouts(self) -> None:
        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.sequence)

        self.right_layout.addWidget(self.option_picker)
        self.right_layout.addWidget(self.graph_editor)

        self.right_layout.setStretchFactor(self.option_picker, 2)
        self.right_layout.setStretchFactor(self.graph_editor, 1)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # Set stretch factors
        self.main_layout.setStretchFactor(self.left_layout, 1)
        self.main_layout.setStretchFactor(self.right_layout, 2)

        self.setLayout(self.main_layout)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

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
        if self.graph_editor.pictograph.selectedItems():
            return self.graph_editor.pictograph

        for beat_view in self.sequence.frame.beats:
            if beat_view.pictograph and beat_view.pictograph.selectedItems():
                return beat_view.pictograph

        return None

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.sequence.update_size()
        # self.option_picker.update_size()
        self.graph_editor.update_graph_editor_size()
