from typing import TYPE_CHECKING, Union
from Enums.PropTypes import PropType

from data.constants import BLUE, DASH, FLOAT, NO_ROT, RED, STATIC
from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
    BeatView,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JSON_Manager


class JsonSequenceUpdater:
    def __init__(self, json_manager: "JSON_Manager"):
        self.json_manager = json_manager
        self.main_widget = json_manager.main_widget

    def update_sequence_properties(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        if len(sequence) > 1:
            sequence_properties_manager = self.main_widget.sequence_properties_manager
            sequence_properties_manager.instantiate_sequence(sequence)
            properties = sequence_properties_manager.check_all_properties()

            # Update the sequence properties in the JSON
            sequence[0]["word"] = properties["word"]
            sequence[0]["author"] = properties["author"]
            sequence[0]["level"] = properties["level"]
            sequence[0]["is_circular"] = properties["is_circular"]
            sequence[0]["is_permutable"] = properties["is_permutable"]
            sequence[0]["is_strictly_rotational_permutation"] = properties[
                "is_strictly_rotational_permutation"
            ]
            sequence[0]["is_strictly_mirrored_permutation"] = properties[
                "is_strictly_mirrored_permutation"
            ]
            sequence[0]["is_strictly_colorswapped_permutation"] = properties[
                "is_strictly_colorswapped_permutation"
            ]
            sequence[0]["is_mirrored_color_swapped_permutation"] = properties[
                "is_mirrored_color_swapped_permutation"
            ]
            sequence[0]["is_rotational_colorswapped_permutation"] = properties[
                "is_rotational_colorswapped_permutation"
            ]

            # Save the updated sequence back to the JSON
            self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prop_type_in_json(self, prop_type: PropType) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[0]["prop_type"] = prop_type.name.lower()
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prefloat_motion_type_in_json(
        self, index: int, color: str, motion_type: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prefloat_motion_type"] = motion_type
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_prefloat_prop_rot_dir_in_json(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"] = prop_rot_dir
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_motion_type_in_json_at_index(
        self, index: int, color: str, motion_type: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["motion_type"] = motion_type
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if "prefloat_motion_type" in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"]["prefloat_motion_type"]

        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_letter_in_json_at_index(self, index: int, letter: str) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index]["letter"] = letter
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_turns_in_json_at_index(
        self, index: int, color: str, turns: Union[int, float]
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.json_manager.ori_calculator.calculate_end_orientation(
            sequence[index], color
        )
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if sequence[index][f"{color}_attributes"]["turns"] > 0:
                pictograph = self.json_manager.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                    index - 2
                ].beat
                if pictograph:
                    motion = pictograph.get.motion_by_color(color)
                    prop_rot_dir = motion.prop_rot_dir
                    sequence[index][f"{color}_attributes"][
                        "prop_rot_dir"
                    ] = prop_rot_dir
            if "prefloat_prop_rot_dir" in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"]
        elif sequence[index][f"{color}_attributes"]["turns"] == "fl":
            pictograph = self.json_manager.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                index - 2
            ].beat
            if pictograph:
                motion = pictograph.get.motion_by_color(color)

        if sequence[index][f"{color}_attributes"]["motion_type"] in [DASH, STATIC]:
            if sequence[index][f"{color}_attributes"]["turns"] == 0:
                prop_rot_dir = NO_ROT
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        self.json_manager.loader_saver.save_current_sequence(sequence)
        self.update_sequence_properties()

    def update_prop_rot_dir_in_json_at_index(
        self, index: int, color: str, prop_rot_dir: str
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir
        # if the turns is not "fl", then delete the prefloat prop_rot_dir
        if sequence[index][f"{color}_attributes"]["turns"] != "fl":
            if "prefloat_prop_rot_dir" in sequence[index][f"{color}_attributes"]:
                del sequence[index][f"{color}_attributes"]["prefloat_prop_rot_dir"]
        self.json_manager.loader_saver.save_current_sequence(sequence)

    def update_current_sequence_file_with_beat(self, beat_view: BeatView):
        sequence_data = self.json_manager.loader_saver.load_current_sequence_json()
        # if len(sequence_data) == 0:  # Make sure there's at least the metadata entry
        #     sequence_data.append(
        #         {
        #             "prop_type": self.json_manager.main_widget.prop_type.name.lower(),
        #             "is_circular": False,
        #         }
        #     )
        sequence_data.append(beat_view.beat.pictograph_dict)
        self.json_manager.loader_saver.save_current_sequence(sequence_data)
        self.update_sequence_properties()  # Recalculate properties after each update
        self.json_manager.main_widget.main_window.settings_manager.save_settings()  # Save state on change

    def clear_and_repopulate_the_current_sequence(self):
        self.json_manager.loader_saver.clear_current_sequence_file()
        beat_frame = (
            self.json_manager.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        beat_views = beat_frame.beats
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.json_manager.start_position_handler.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view)
        self.json_manager.main_widget.main_window.settings_manager.save_settings()  # Save state on change

    def set_turns_from_num_to_num_in_json(self, motion: "Motion", new_turns):
        beat_index = (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
        )
        json_index = beat_index + 2
        self.update_turns_in_json_at_index(json_index, motion.color, new_turns)
        self.update_motion_type_in_json_at_index(
            json_index, motion.color, motion.motion_type
        )

        self.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, motion.prop_rot_dir
        )

    def set_turns_to_num_from_fl_in_json(self, motion: "Motion", new_turns):
        beat_index = (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
        )
        json_index = beat_index + 2
        motion.motion_type = (
            self.json_manager.loader_saver.get_prefloat_motion_type_from_json_at_index(
                json_index,
                motion.color,
            )
        )
        motion.prop_rot_dir = (
            self.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                json_index,
                motion.color,
            )
        )
        self.update_turns_in_json_at_index(json_index, motion.color, new_turns)
        self.update_motion_type_in_json_at_index(
            json_index, motion.color, motion.motion_type
        )
        self.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, motion.prop_rot_dir
        )

    def set_turns_to_fl_from_num_in_json(self, motion: "Motion", new_turns):
        beat_index = (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
        )
        json_index = beat_index + 2
        self.update_turns_in_json_at_index(json_index, motion.color, new_turns)
        self.update_prefloat_motion_type_in_json(
            json_index,
            motion.color,
            self.json_manager.loader_saver.get_motion_type_from_json_at_index(
                json_index, motion.color
            ),
        )
        self.update_prefloat_prop_rot_dir_in_json(
            json_index,
            motion.color,
            self.json_manager.loader_saver.get_prop_rot_dir_from_json(
                json_index, motion.color
            ),
        )
        self.update_motion_type_in_json_at_index(json_index, motion.color, FLOAT)
        self.update_prop_rot_dir_in_json_at_index(json_index, motion.color, NO_ROT)
