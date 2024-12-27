from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem

from main_window.main_widget.sequence_widget.graph_editor_placeholder import (
    GraphEditorPlaceholder,
)

from .sequence_color_swap_manager import SequenceColorSwapManager
from .sequence_mirror_manager import SequenceMirrorManager
from .sequence_rotation_manager import SequenceRotationManager
from .graph_editor.graph_editor_toggle_tab import GraphEditorToggleTab
from .graph_editor.graph_editor_animator import GraphEditorAnimator
from .sequence_clearer import SequenceClearer
from .sequence_widget_layout_manager import SequenceWidgetLayoutManager
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWidgetBeatFrame
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
    graph_editor_placeholder: "QSpacerItem"

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

        # Graph Editor
        self.graph_editor = GraphEditor(self)
        self.graph_editor_placeholder = GraphEditorPlaceholder(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.toggler = GraphEditorAnimator(self)

        # Layout
        self.layout_manager = SequenceWidgetLayoutManager(self)

    def resizeEvent(self, event):
        self.toggle_tab.reposition_toggle_tab()
        super().resizeEvent(event)
