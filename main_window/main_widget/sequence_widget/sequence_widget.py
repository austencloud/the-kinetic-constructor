from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.main_widget.sequence_widget.beat_deleter import (
    BeatDeleter,
)
from .full_screen_viewer import FullScreenViewer
from .sequence_color_swapper import SequenceColorSwapper
from .sequence_reflector import SequenceReflector
from .sequence_rotater import SequenceRotater
from .sequence_widget_layout_manager import SequenceWidgetLayoutManager
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_beat_frame import SequenceBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .labels.sequence_widget_indicator_label import SequenceWidgetIndicatorLabel
from .sequence_widget_button_panel import SequenceWidgetButtonPanel
from .sequence_widget_scroll_area import SequenceWidgetScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceWidget(QWidget):
    beat_frame_layout: QHBoxLayout
    indicator_label_layout: QHBoxLayout

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

        # Managers
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.autocompleter = SequenceAutoCompleter(self)

        # Modification Managers
        self.mirror_manager = SequenceReflector(self)
        self.color_swap_manager = SequenceColorSwapper(self)
        self.rotation_manager = SequenceRotater(self)

        # Labels
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

        # Sections
        self.scroll_area = SequenceWidgetScrollArea(self)
        self.beat_frame = SequenceBeatFrame(self)
        self.button_panel = SequenceWidgetButtonPanel(self)
        self.graph_editor = GraphEditor(self)

        # Full Screen Viewer
        self.full_screen_viewer = FullScreenViewer(self)

        # Layout
        self.layout_manager = SequenceWidgetLayoutManager(self)
        self.beat_deleter = BeatDeleter(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_editor.toggle_tab.reposition_toggle_tab()
