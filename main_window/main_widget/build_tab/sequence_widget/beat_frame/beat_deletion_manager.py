from typing import TYPE_CHECKING

from main_window.main_widget.build_tab.sequence_widget.beat_frame.beat_view import (
    BeatView,
)
from main_window.main_widget.build_tab.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)


if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatDeletionManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.manual_builder = None
        self.selection_overlay = self.beat_frame.selection_overlay
        self.json_manager = self.beat_frame.json_manager  # Access json manager
        self.settings_manager = self.beat_frame.settings_manager

    def delete_selected_beat(self) -> None:
        """Delete the currently selected beat."""
        self.beats = self.beat_frame.beats
        self._initialize_manual_builder()
        self._initialize_GE_pictograph_view()

        selected_beat = self.beat_frame.selection_overlay.get_selected_beat()
        if not selected_beat:
            self._show_no_beat_selected_message()
            return

        self._delete_beat_based_on_type(selected_beat)
        self._post_deletion_updates()

    def _initialize_manual_builder(self) -> None:
        """Initialize the manual builder if not already initialized."""
        if not self.manual_builder:
            self.manual_builder = (
                self.beat_frame.main_widget.build_tab.sequence_constructor
            )

    def _initialize_GE_pictograph_view(self) -> None:
        """Initialize the GE pictograph view."""
        self.GE_pictograph_view = (
            self.beat_frame.main_widget.build_tab.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view
        )

    def _show_no_beat_selected_message(self) -> None:
        """Show a message indicating no beat is selected."""
        self.sequence_widget = self.beat_frame.main_widget.build_tab.sequence_widget
        message = "You can't delete a beat if you haven't selected one."
        self.sequence_widget.indicator_label.show_message(message)

    def _delete_beat_based_on_type(self, selected_beat: BeatView) -> None:
        """Delete the beat based on its type."""
        if selected_beat.__class__ == StartPositionBeatView:
            self._delete_start_pos()
        elif selected_beat == self.beats[0]:
            self._delete_first_beat(selected_beat)
        else:
            self._delete_non_first_beat(selected_beat)

    def _post_deletion_updates(self) -> None:
        """Perform updates after deletion."""
        self.json_manager.updater.clear_and_repopulate_the_current_sequence()
        if self.settings_manager.global_settings.get_grow_sequence():
            self.beat_frame.layout_manager.adjust_layout_to_sequence_length()
        self.beat_frame.sequence_widget.current_word_label.update_current_word_label_from_beats()
        self.manual_builder.option_picker.update_option_picker()

    def _delete_non_first_beat(self, selected_beat: BeatView) -> None:
        """Delete a non-first beat."""
        self.delete_beat(selected_beat)
        for i in range(self.beats.index(selected_beat), len(self.beats)):
            self.delete_beat(self.beats[i])
        last_beat = self.beat_frame.get.last_filled_beat()
        self.selection_overlay.select_beat(last_beat)
        self.manual_builder.last_beat = last_beat.beat

    def _delete_first_beat(self, selected_beat: BeatView) -> None:
        """Delete the first beat."""
        self.start_pos_view = self.beat_frame.start_pos_view
        self.selection_overlay.select_beat(self.start_pos_view)
        self.manual_builder.last_beat = self.start_pos_view.beat
        self.delete_beat(selected_beat)

        for i in range(self.beats.index(selected_beat) + 1, len(self.beats)):
            self.delete_beat(self.beats[i])

        self.sequence_widget = self.beat_frame.main_widget.build_tab.sequence_widget
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _delete_start_pos(self) -> None:
        """Delete the start position beat."""
        self.start_pos_view = self.beat_frame.start_pos_view
        self.start_pos_view.setScene(self.start_pos_view.blank_beat)
        self.start_pos_view.is_filled = False
        self.GE_pictograph_view.set_to_blank_grid()
        for beat in self.beats:
            self.delete_beat(beat)
        self.selection_overlay.deselect_beat()
        self.json_manager.sequence_loader_saver.clear_current_sequence_file()
        self.manual_builder.last_beat = None
        self.manual_builder.reset_to_start_pos_picker()
        self.manual_builder.option_picker.update_option_picker()
        graph_editor = (
            self.beat_frame.main_widget.build_tab.sequence_widget.graph_editor
        )
        graph_editor.adjustment_panel.update_adjustment_panel()

    def delete_beat(self, beat_view: BeatView) -> None:
        """Delete a specific beat."""
        beat_view.setScene(beat_view.blank_beat)
        beat_view.is_filled = False

    def delete_all_beats(self) -> None:
        """Delete all beats."""
        self.beats = self.beat_frame.beats
        self._initialize_manual_builder()
        self._initialize_GE_pictograph_view()
        self._delete_start_pos()
        self._post_deletion_updates()
