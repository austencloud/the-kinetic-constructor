from copy import deepcopy
from PyQt6.QtCore import QObject, pyqtSignal
from widgets.pictograph.pictograph import Pictograph
from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from widgets.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )


class AdvancedStartPosManager(QObject):
    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker") -> None:
        super().__init__()
        self.sequence_builder = advanced_start_pos_picker.sequence_builder
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.pictograph_frame = advanced_start_pos_picker.pictograph_frame
        self.main_widget = advanced_start_pos_picker.sequence_builder.builder_toolbar
        self.start_pos_cache = advanced_start_pos_picker.start_pos_cache

    def on_start_pos_clicked(self, clicked_start_option: Pictograph) -> None:
        start_position_beat = StartPositionBeat(
            self.sequence_builder.builder_toolbar,
            self.sequence_builder.builder_toolbar.sequence_widget.beat_frame,
        )
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )
        self.sequence_builder.builder_toolbar.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_position_beat
        )
        self.sequence_builder.current_pictograph = start_position_beat
        beat_frame = self.sequence_builder.builder_toolbar.sequence_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_manager.select_beat(start_pos_view)

        QApplication.processEvents()
        self.start_position_selected.connect(
            self.sequence_builder.transition_to_sequence_building
        )
        self.sequence_builder.builder_toolbar.json_manager.current_sequence_json_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def hide_start_positions(self) -> None:
        for start_position_pictograph in self.start_pos_cache.values():
            start_position_pictograph.view.hide()

    def update_left_default_ori(self, left_ori: str):
        for (
            start_pos_pictographs_by_letter
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for pictograph in start_pos_pictographs_by_letter:
                pictograph.pictograph_dict["blue_attributes"]["start_ori"] = left_ori
                pictograph.pictograph_dict["red_attributes"]["blue_ori"] = left_ori
                pictograph.updater.update_pictograph(pictograph.pictograph_dict)

    def update_right_default_ori(self, right_ori: str):
        for (
            start_pos_pictographs_by_letter
        ) in self.advanced_start_pos_picker.start_pos_cache.values():
            for pictograph in start_pos_pictographs_by_letter:
                pictograph.pictograph_dict["red_attributes"]["start_ori"] = right_ori
                pictograph.pictograph_dict["red_attributes"]["end_ori"] = right_ori
                pictograph.updater.update_pictograph(pictograph.pictograph_dict)
