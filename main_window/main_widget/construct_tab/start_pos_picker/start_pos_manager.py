from copy import deepcopy
from functools import partial
from PyQt6.QtCore import QObject, pyqtSignal
from Enums.letters import Letter
from data.constants import BOX, DIAMOND, END_POS, START_POS
from base_widgets.base_pictograph.pictograph import Pictograph
from data.position_maps import box_positions, diamond_positions

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.sequence_workbench.beat_frame.start_pos_beat import (
    StartPositionBeat,
)

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__()
        self.start_pos_picker = start_pos_picker
        self.construct_tab = start_pos_picker.construct_tab
        self.main_widget = self.construct_tab.main_widget
        self.start_pos_frame = start_pos_picker.pictograph_frame

        self.top_builder_widget = None
        self.box_pictographs: list[Pictograph] = []
        self.diamond_pictographs: list[Pictograph] = []
        self.start_options: dict[str, Pictograph] = {}

        self.start_position_selected.connect(
            self.construct_tab.transition_to_option_picker
        )

        self.load_relevant_start_positions()

    def get_all_start_positions(self) -> list[Pictograph]:
        return self.box_pictographs + self.diamond_pictographs

    def clear_start_positions(self) -> None:
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def load_relevant_start_positions(self, grid_mode: str = None) -> None:
        if not grid_mode:
            grid_mode = DIAMOND

        if grid_mode == BOX:
            self.box_pictographs = self.get_box_variations()
            for position_key in ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]:
                self._add_start_position_option_to_start_pos_frame(position_key, BOX)
        elif grid_mode == DIAMOND:
            self.diamond_pictographs = self.get_diamond_variations()
            for position_key in ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]:
                self._add_start_position_option_to_start_pos_frame(
                    position_key, DIAMOND
                )

    def get_box_variations(self) -> list[Pictograph]:
        box_variations = []
        for letter, pictograph_datas in self.main_widget.pictograph_datas.items():
            for pictograph_data in pictograph_datas:
                if pictograph_data["start_pos"] in box_positions:
                    pictograph = self.create_pictograph_from_dict(pictograph_data, BOX)
                    box_variations.append(pictograph)

        return box_variations

    def get_diamond_variations(self) -> list[Pictograph]:
        diamond_variations = []
        for letter, pictograph_datas in self.main_widget.pictograph_datas.items():
            for pictograph_data in pictograph_datas:
                if pictograph_data["start_pos"] in diamond_positions:
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_data, DIAMOND
                    )
                    diamond_variations.append(pictograph)

        return diamond_variations

    def _add_start_position_option_to_start_pos_frame(
        self, position_key: str, grid_mode: str
    ) -> None:
        start_pos, end_pos = position_key.split("_")

        for letter, pictograph_datas in self.main_widget.pictograph_datas.items():
            for pictograph_data in pictograph_datas:
                if (
                    pictograph_data[START_POS] == start_pos
                    and pictograph_data[END_POS] == end_pos
                ):
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_data, grid_mode
                    )
                    self.start_options[letter] = pictograph

                    pictograph.letter = letter
                    pictograph.start_pos = start_pos
                    pictograph.end_pos = end_pos
                    self.start_pos_frame._add_start_pos_to_layout(pictograph)

                    pictograph.view.mousePressEvent = partial(
                        self.add_start_pos_to_sequence, pictograph
                    )

                    pictograph.start_to_end_pos_glyph.hide()

    def add_start_pos_to_sequence(
        self, clicked_start_option: Pictograph, event: QWidget = None
    ) -> None:
        seq_widget = self.main_widget.sequence_workbench
        start_position_beat = StartPositionBeat(seq_widget.beat_frame)

        clicked_start_option.updater.update_dict_from_attributes()

        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_data)
        )

        seq_widget.beat_frame.start_pos_view.set_start_pos(start_position_beat)
        self.construct_tab.last_beat = start_position_beat

        beat_frame = seq_widget.beat_frame
        start_pos_view = beat_frame.start_pos_view
        beat_frame.selection_overlay.select_beat(start_pos_view)

        self.main_widget.json_manager.start_pos_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)

    def hide_start_positions(self) -> None:
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget.sequence_workbench.beat_frame
        )

        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_data
        )
        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "Pictograph":
        if not start_pos_data:
            return None

        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.pictograph_datas.get(letter, [])

        for pictograph_data in matching_letter_pictographs:
            if pictograph_data["start_pos"] == start_pos_key:
                pictograph_data["blue_attributes"]["start_ori"] = start_pos_data[
                    "blue_attributes"
                ]["end_ori"]
                pictograph_data["red_attributes"]["start_ori"] = start_pos_data[
                    "red_attributes"
                ]["end_ori"]

                pictograph_factory = (
                    self.main_widget.sequence_workbench.beat_frame.beat_factory
                )
                pictograph_key = (
                    self.main_widget.pictograph_key_generator.generate_pictograph_key(
                        pictograph_data
                    )
                )
                start_pos_pictograph = pictograph_factory.create_start_pos_beat(
                    pictograph_key, pictograph_data
                )
                return start_pos_pictograph

        raise ValueError("No matching start position pictograph found")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str) -> str:
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None

    def create_pictograph_from_dict(
        self, pictograph_data: dict, target_grid_mode: str
    ) -> Pictograph:
        local_dict = deepcopy(pictograph_data)
        local_dict["grid_mode"] = target_grid_mode

        pictograph = Pictograph(self.main_widget)
        pictograph.updater.update_pictograph(local_dict)

        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        else:
            self.diamond_pictographs.append(pictograph)

        return pictograph

    def reinitialize_pictographs(self, new_grid_mode: str = None):
        self.clear_start_positions()
        self.start_options.clear()
        self.box_pictographs.clear()
        self.diamond_pictographs.clear()

        if new_grid_mode:
            self.load_relevant_start_positions(new_grid_mode)
        else:
            self.load_relevant_start_positions()
