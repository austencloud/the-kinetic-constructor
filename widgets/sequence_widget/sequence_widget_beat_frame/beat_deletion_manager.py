from typing import TYPE_CHECKING

from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
    StartPositionBeatView,
)


if TYPE_CHECKING:
    pass

from widgets.sequence_widget.sequence_widget_beat_frame.beat import BeatView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
<<<<<<< HEAD:widgets/sequence_widget/sequence_beat_frame/beat_deletion_manager.py
    from widgets.sequence_widget.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
=======
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409:widgets/sequence_widget/sequence_widget_beat_frame/beat_deletion_manager.py
    )


class BeatDeletionManager:
    def __init__(self, sequence_beat_frame: "SequenceBeatFrame"):
        self.beat_frame = sequence_beat_frame
        self.beats = sequence_beat_frame.beat_views
        self.start_pos_view = self.beat_frame.start_pos_view
        self.sequence_builder = (
            self.beat_frame.sequence_widget.main_widget.main_tab_widget.sequence_builder
        )
        self.selection_manager = self.beat_frame.selection_manager
        self.current_sequence_json_handler = (
            self.beat_frame.current_sequence_json_handler
        )

    def delete_selected_beat(self):
        GE_pictograph_view = (
            self.beat_frame.sequence_widget.sequence_modifier.graph_editor.GE_pictograph_view
        )
        selected_beat = self.beat_frame.selection_manager.get_selected_beat()

        if selected_beat.__class__ == StartPositionBeatView:
            self.start_pos_view.setScene(None)
            self.start_pos_view.is_filled = False
            GE_pictograph_view.set_to_blank_grid()
            for beat in self.beats:
                self.delete_beat(beat)
            self.selection_manager.deselect_beat()
            self.current_sequence_json_handler.clear_current_sequence_file()
            self.sequence_builder.current_pictograph = None
            self.sequence_builder.reset_to_start_pos_picker()
            self.sequence_builder.option_picker.update_option_picker()

        elif selected_beat:
            if selected_beat == self.beats[0]:
                self.selection_manager.select_beat(self.start_pos_view)
                last_beat = self.start_pos_view
                self.sequence_builder.current_pictograph = self.start_pos_view.beat
                self.delete_beat(selected_beat)

                for i in range(
                    self.beats.index(selected_beat) + 1,
                    len(self.beats),
                ):

                    self.delete_beat(self.beats[i])

                self.current_sequence_json_handler.clear_and_repopulate_the_current_sequence()

            else:
                self.delete_beat(selected_beat)
                for i in range(self.beats.index(selected_beat), len(self.beats)):
                    self.delete_beat(self.beats[i])
                last_beat = self.beat_frame.get_last_filled_beat()
                self.selection_manager.select_beat(last_beat)
                self.sequence_builder.current_pictograph = last_beat.beat
            self.current_sequence_json_handler.clear_and_repopulate_the_current_sequence()
            self.sequence_builder.option_picker.update_option_picker()

    def delete_beat(self, beat_view: BeatView) -> None:
        beat_view.setScene(None)
        beat_view.is_filled = False
