from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QFrame,
    QTabWidget, QApplication
)
from PyQt6.QtGui import QWheelEvent
from utilities.TypeChecking.TypeChecking import LetterDictionary
from utilities.json_handler import JsonHandler
from widgets.graph_editor.graph_editor_widget import GraphEditorWidget
from widgets.graph_editor.key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from widgets.option_picker.option_picker_widget import OptionPickerWidget
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow
from PyQt6.QtGui import QResizeEvent


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

        self.graph_editor_widget = GraphEditorWidget(self)
        self.sequence_widget = SequenceWidget(self)
        self.option_picker_widget = OptionPickerWidget(self)

        self.configure_layouts()

    def configure_layouts(self) -> None:
        self.horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.left_frame = QFrame()
        self.right_frame = QFrame()

        self.right_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.left_layout = QVBoxLayout(self.left_frame)
        self.right_layout = QVBoxLayout(self.right_frame)

        self.left_layout.addWidget(self.sequence_widget)

        # Instead of a vertical splitter, use a QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.option_picker_widget, "Option Picker")
        self.tab_widget.addTab(self.graph_editor_widget, "Graph Editor")
        # self.tab_widget.currentChanged.connect(self.on_tab_changed)

        # Get screen size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()

        # Calculate the size for the main window and right frame
        main_window_width = int(screen_size.width() * 0.75)
        main_window_height = int(screen_size.height() * 0.75)
        right_frame_initial_width = int(main_window_width * 0.6)  # Example value, adjust as needed

        # self.main_window.resize(main_window_width, main_window_height)
        self.right_frame.setFixedWidth(right_frame_initial_width)
        self.right_layout.addWidget(self.tab_widget)
        

        # Add frames to the horizontal splitter
        self.horizontal_splitter.addWidget(self.left_frame)
        self.horizontal_splitter.addWidget(self.right_frame)
        self.horizontal_splitter.splitterMoved.connect(self.on_splitter_moved)

        # Optionally, set initial sizes or proportions for the splitters
        self.horizontal_splitter.setSizes([300, 500])

        # Create main layout and add the horizontal splitter
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.horizontal_splitter)
        self.setLayout(self.main_layout)

    ### EVENT HANDLERS ###

    def on_splitter_moved(self):
        # This method is called whenever the splitter is moved
        self.option_picker_widget.resize_option_picker_widget()
        self.sequence_widget.resize_sequence_widget()

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            active_pictograph = self.find_active_pictograph()
            if active_pictograph:
                self.key_event_handler.keyPressEvent(event, self, active_pictograph)
                return True

        return super().eventFilter(source, event)

    def deselect_all_except(self, active_pictograph: Pictograph) -> None:
        if self.graph_editor_widget.graph_editor.main_pictograph != active_pictograph:
            self.graph_editor_widget.graph_editor.main_pictograph.clearSelection()

        for beat_view in self.sequence_widget.beat_frame.beats:
            if beat_view.pictograph and beat_view.pictograph != active_pictograph:
                beat_view.pictograph.clearSelection()

    def find_active_pictograph(self) -> Optional[Pictograph]:
        if self.graph_editor_widget.graph_editor.main_pictograph.selectedItems():
            return self.graph_editor_widget.graph_editor.main_pictograph

        for beat_view in self.sequence_widget.beat_frame.beats:
            if beat_view.pictograph and beat_view.pictograph.selectedItems():
                return beat_view.pictograph

        return None

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        return super().wheelEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.option_picker_widget.resize_option_picker_widget()
        # self.sequence_widget.resize_sequence_widget()
