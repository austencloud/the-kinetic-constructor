from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .sequence_color_swap_manager import SequenceColorSwapManager
from .sequence_mirror_manager import SequenceMirrorManager
from .sequence_rotation_manager import SequenceRotationManager
from .sequence_clearer import SequenceClearer
from .sequence_widget_layout_manager import SequenceWidgetLayoutManager
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWidgetBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .sequence_widget_indicator_label import SequenceWidgetIndicatorLabel
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
        self.sequence_clearer = SequenceClearer(self)

        # Modification Managers
        self.mirror_manager = SequenceMirrorManager(self)
        self.color_swap_manager = SequenceColorSwapManager(self)
        self.rotation_manager = SequenceRotationManager(self)

        # Labels
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

        # Sections
        self.scroll_area = SequenceWidgetScrollArea(self)
        self.beat_frame = SequenceWidgetBeatFrame(self)
        self.button_panel = SequenceWidgetButtonPanel(self)
        self.graph_editor = GraphEditor(self)

        # Layout
        self.layout_manager = SequenceWidgetLayoutManager(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_editor.toggle_tab.reposition_toggle_tab()
