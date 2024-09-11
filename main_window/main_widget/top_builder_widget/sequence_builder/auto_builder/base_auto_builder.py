from typing import TYPE_CHECKING
import random


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_auto_builder_frame import (
        BaseAutoBuilderFrame,
    )


class BaseAutoBuilder:
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        self.auto_builder_frame = auto_builder_frame
        self.sequence_widget: "SequenceWidget" = None
        self.top_builder_widget = (
            auto_builder_frame.auto_builder.sequence_builder.top_builder_widget
        )
        self.main_widget = self.top_builder_widget.main_widget
        self.validation_engine = self.main_widget.json_manager.validation_engine
        self.sequence_builder = self.top_builder_widget.sequence_builder

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def add_start_pos_pictograph(self):
        start_pos_keys = [
            f"{prefix}{i}_{prefix}{i}"
            for prefix in ["alpha", "beta", "gamma"]
            for i in range(1, 5 if prefix != "gamma" else 9)
        ]
        position_key = random.choice(start_pos_keys)
        self._add_start_position_to_sequence(position_key)

    def _add_start_position_to_sequence(self, position_key: str) -> None:
        start_pos, end_pos = position_key.split("_")
        start_pos_picker = (
            self.main_widget.top_builder_widget.sequence_builder.manual_builder.start_pos_picker
        )
        start_pos_manager = start_pos_picker.start_pos_manager
        for (
            letter,
            pictograph_dicts,
        ) in self.sequence_widget.main_widget.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict["start_pos"] == start_pos
                    and pictograph_dict["end_pos"] == end_pos
                ):
                    start_position_pictograph = (
                        start_pos_picker.pictograph_factory.create_pictograph()
                    )
                    start_position_pictograph.letter = letter
                    start_position_pictograph.start_pos = start_pos
                    start_position_pictograph.end_pos = end_pos
                    start_position_pictograph.updater.update_pictograph(pictograph_dict)
                    start_pos_manager.add_start_pos_to_sequence(
                        start_position_pictograph
                    )
                    return

    def _update_start_oris(self, next_pictograph_dict, last_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["start_ori"] = last_pictograph_dict[
            "blue_attributes"
        ]["end_ori"]
        next_pictograph_dict["red_attributes"]["start_ori"] = last_pictograph_dict[
            "red_attributes"
        ]["end_ori"]

    def _update_end_oris(self, next_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["end_ori"] = (
            self.sequence_widget.main_widget.json_manager.ori_calculator.calculate_end_orientation(
                next_pictograph_dict, "blue"
            )
        )
        next_pictograph_dict["red_attributes"]["end_ori"] = (
            self.sequence_widget.main_widget.json_manager.ori_calculator.calculate_end_orientation(
                next_pictograph_dict, "red"
            )
        )

    def _filter_options_by_rotation(
        self, options: list[dict], blue_rot_dir, red_rot_dir
    ) -> list[dict]:
        """Filter options to match the rotation direction for both hands."""
        filtered_options = []
        for option in options:
            if option["blue_attributes"]["prop_rot_dir"] in [
                blue_rot_dir,
                "no_rot",
            ] and option["red_attributes"]["prop_rot_dir"] in [red_rot_dir, "no_rot"]:
                filtered_options.append(option)
        return filtered_options if filtered_options else options

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_or_3_constraints(
        self, pictograph: dict, turn_blue: float, turn_red: float
    ) -> dict:
        pictograph["blue_attributes"]["turns"] = turn_blue
        pictograph["red_attributes"]["turns"] = turn_red
        return pictograph

    def _update_dash_static_prop_rot_dirs(
        self, next_pictograph_dict, is_continuous_rot_dir, red_rot_dir, blue_rot_dir
    ):
        if next_pictograph_dict["blue_attributes"]["motion_type"] in ["dash", "static"]:
            if is_continuous_rot_dir:
                next_pictograph_dict["blue_attributes"]["prop_rot_dir"] = (
                    blue_rot_dir
                    if next_pictograph_dict["blue_attributes"]["turns"] > 0
                    else "no_rot"
                )

        if next_pictograph_dict["red_attributes"]["motion_type"] in ["dash", "static"]:
            if is_continuous_rot_dir:
                next_pictograph_dict["red_attributes"]["prop_rot_dir"] = (
                    red_rot_dir
                    if next_pictograph_dict["red_attributes"]["turns"] > 0
                    else "no_rot"
                )
