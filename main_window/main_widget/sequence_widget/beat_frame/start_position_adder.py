from typing import TYPE_CHECKING
from copy import deepcopy

from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class StartPositionAdder:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.sequence_widget = beat_frame.sequence_widget
        self.main_widget = beat_frame.main_widget
        self.json_manager = self.main_widget.json_manager

    def add_start_pos_to_sequence(self, clicked_start_option: "BasePictograph") -> None:
        """Handle adding the start position to the sequence."""
        start_position_beat = StartPositionBeat(self.beat_frame)
        clicked_start_option.updater.update_dict_from_attributes()
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )

        self.beat_frame.start_pos_view.set_start_pos(start_position_beat)
        self.main_widget.construct_tab.last_beat = start_position_beat
        start_pos_view = self.beat_frame.start_pos_view
        self.beat_frame.selection_overlay.select_beat(
            start_pos_view, toggle_graph_editor=False
        )

        self.json_manager.start_position_handler.set_start_position_data(
            start_position_beat
        )
        self.main_widget.construct_tab.start_position_picked = True
        self.main_widget.construct_tab.start_pos_picker.start_position_selected.emit(start_position_beat)
