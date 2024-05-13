from typing import TYPE_CHECKING
from ..SW_beat_frame.start_pos_beat import StartPositionBeatView
from ..SW_beat_frame.beat import BeatView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .SW_beat_frame import SW_BeatFrame


class BeatDeletionManager:
    def __init__(self, sequence_builder_beat_frame: "SW_BeatFrame") -> None:
        self.beat_frame = sequence_builder_beat_frame
        self.beats = sequence_builder_beat_frame.beats
        self.sequence_builder = (
            sequence_builder_beat_frame.top_builder_widget.sequence_builder
        )
        self.selection_manager = self.beat_frame.selection_manager
        self.current_sequence_json_handler = (
            self.beat_frame.current_sequence_json_handler
        )

    def delete_selected_beat(self) -> None:
        self.GE_pictograph_view = (
            self.beat_frame.main_widget.top_builder_widget.sequence_widget.graph_editor.graph_editor.GE_pictograph_view
        )
        selected_beat = self.beat_frame.selection_manager.get_selected_beat()

        if selected_beat.__class__ == StartPositionBeatView:
            self._delete_start_pos()
        elif selected_beat == self.beats[0]:
            self._delete_first_beat(selected_beat)
        else:
            self._delete_non_first_beat(selected_beat)

        self.current_sequence_json_handler.clear_and_repopulate_the_current_sequence()
        self.sequence_builder.option_picker.update_option_picker()

    def _delete_non_first_beat(self, selected_beat):
        self.delete_beat(selected_beat)
        for i in range(self.beats.index(selected_beat), len(self.beats)):
            self.delete_beat(self.beats[i])
        last_beat = self.beat_frame.get_last_filled_beat()
        self.selection_manager.select_beat(last_beat)
        self.sequence_builder.current_pictograph = last_beat.beat

    def _delete_first_beat(self, selected_beat):
        self.start_pos_view = self.beat_frame.start_pos_view
        self.selection_manager.select_beat(self.start_pos_view)
        self.sequence_builder.current_pictograph = self.start_pos_view.beat
        self.delete_beat(selected_beat)

        for i in range(
            self.beats.index(selected_beat) + 1,
            len(self.beats),
        ):
            self.delete_beat(self.beats[i])

    def _delete_start_pos(self):
        self.start_pos_view = self.beat_frame.start_pos_view
        self.start_pos_view.setScene(None)
        self.start_pos_view.is_filled = False
        self.GE_pictograph_view.set_to_blank_grid()
        for beat in self.beats:
            self.delete_beat(beat)
        self.selection_manager.deselect_beat()
        self.current_sequence_json_handler.clear_current_sequence_file()
        self.sequence_builder.current_pictograph = None
        self.sequence_builder.reset_to_start_pos_picker()
        self.sequence_builder.option_picker.update_option_picker()
        graph_editor = (
            self.beat_frame.main_widget.top_builder_widget.sequence_widget.graph_editor.graph_editor
        )
        graph_editor.adjustment_panel.update_adjustment_panel()

    def delete_beat(self, beat_view: BeatView) -> None:
        beat_view.setScene(None)
        beat_view.is_filled = False
