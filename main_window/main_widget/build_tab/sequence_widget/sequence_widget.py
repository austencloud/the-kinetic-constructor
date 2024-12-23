from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem

from main_window.main_widget.build_tab.sequence_widget.sequence_color_swap_manager import (
    SequenceColorSwapManager,
)
from main_window.main_widget.build_tab.sequence_widget.sequence_mirror_manager import (
    SequenceMirrorManager,
)
from main_window.main_widget.build_tab.sequence_widget.sequence_rotation_manager import (
    SequenceRotationManager,
)
from .graph_editor.graph_editor_toggle_tab import GraphEditorToggleTab
from .graph_editor.graph_editor_toggler import GraphEditorToggler
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
    from main_window.main_widget.build_tab.build_tab import BuildTab
    from main_window.main_widget.main_widget import MainWidget


class SequenceWidget(QWidget):
    beat_frame_layout: QHBoxLayout
    indicator_label_layout: QHBoxLayout
    graph_editor_placeholder: "QSpacerItem"

    def __init__(self, build_tab: "BuildTab") -> None:
        super().__init__()
        self.main_widget = build_tab.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.json_manager = self.main_widget.json_manager
        self.default_beat_quantity = 16

        # Initialize managers
        self.mirror_manager = SequenceMirrorManager(self)
        self.color_swap_manager = SequenceColorSwapManager(self)
        self.rotation_manager = SequenceRotationManager(self)

        self._setup_components()
        self.layout_manager.setup_layout()

    def update_beats_in_place(self, modified_sequence_json):
        self.json_manager.loader_saver.save_current_sequence(modified_sequence_json)
        self.json_manager.ori_validation_engine.run(is_current_sequence=True)

        self.update_beats(modified_sequence_json)
        self.update_beats(modified_sequence_json)

        self.current_word_label.update_current_word_label_from_beats()
        self.difficulty_label.update_difficulty_label()

        currently_selected_beat = self.beat_frame.selection_overlay.selected_beat
        blue_motion = currently_selected_beat.beat.blue_motion
        red_motion = currently_selected_beat.beat.red_motion
        self.graph_editor.adjustment_panel.update_turns_panel(blue_motion, red_motion)

    def update_beats(self, modified_sequence_json: list[dict]):
        if len(modified_sequence_json) > 1:
            start_pos_dict = modified_sequence_json[1]
            start_pos = self.beat_frame.start_pos_view.start_pos
            start_pos.updater.update_pictograph(start_pos_dict)
            # start_pos.updater.update_motions(start_pos_dict)
            grid_mode = self.main_widget.grid_mode_checker.get_grid_mode(start_pos_dict)
            start_pos.grid.hide()
            start_pos.grid.__init__(start_pos, start_pos.grid.grid_data, grid_mode)

        for i, beat_dict in enumerate(modified_sequence_json[2:], start=0):
            if i < len(self.beat_frame.beats) and self.beat_frame.beats[i].is_filled:
                beat = self.beat_frame.beats[i].beat
                beat.updater.update_pictograph(beat_dict)
                # beat.updater.update_motions(beat_dict)
                grid_mode = self.main_widget.grid_mode_checker.get_grid_mode(beat_dict)
                beat.grid.hide()
                beat.grid.__init__(beat, beat.grid.grid_data, grid_mode)
            else:
                break

    def _setup_components(self) -> None:
        # Managers
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.autocompleter = SequenceAutoCompleter(self)
        self.sequence_clearer = SequenceClearer(self)
        self.layout_manager = SequenceWidgetLayoutManager(self)

        # Labels
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

        # Sections
        self.scroll_area = SequenceWidgetScrollArea(self)
        self.beat_frame = SequenceWidgetBeatFrame(self)
        self.button_panel = SequenceWidgetButtonPanel(self)

        self.graph_editor = GraphEditor(self)

        # Initialize the toggle tab and toggler
        self.toggle_tab = GraphEditorToggleTab(self)
        self.toggler = GraphEditorToggler(self)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.toggle_tab.reposition_toggle_tab()
        self.graph_editor.resize_graph_editor()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.current_word_label.update_current_word_label_from_beats()
