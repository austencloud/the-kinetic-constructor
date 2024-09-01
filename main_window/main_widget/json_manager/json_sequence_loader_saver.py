import json
from typing import TYPE_CHECKING, List, Dict
from utilities.path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JSON_Manager


class JsonSequenceLoaderSaver:
    def __init__(self, json_manager: "JSON_Manager") -> None:
        self.json_manager = json_manager
        self.current_sequence_json = get_user_editable_resource_path(
            "current_sequence.json"
        )

    def load_current_sequence_json(self) -> List[Dict]:
        try:
            with open(self.current_sequence_json, "r", encoding="utf-8") as file:
                sequence = json.load(file)
            return sequence
        except FileNotFoundError:
            print("Current sequence json not found")
            return [
                {
                    "word": "",
                    "author": self.json_manager.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
                    "level": 0,
                    "prop_type": self.json_manager.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                    "is_strictly_rotational_permutation": False,
                    "is_strictly_mirrored_permutation": False,
                    "is_strictly_colorswapped_permutation": False,
                    "is_mirrored_color_swapped_permutation": False,
                    "is_rotational_colorswapped_permutation": False,
                }
            ]

    def save_current_sequence(self, sequence: List[Dict]):
        if not sequence:
            sequence = [
                {
                    "word": "",
                    "author": self.json_manager.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
                    "level": 0,
                    "prop_type": self.json_manager.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                    "is_strictly_rotational_permutation": False,
                    "is_strictly_mirrored_permutation": False,
                    "is_strictly_colorswapped_permutation": False,
                    "is_mirrored_color_swapped_permutation": False,
                    "is_rotational_colorswapped_permutation": False,
                }
            ]
        else:
            if "word" not in sequence[0]:
                sequence[0][
                    "word"
                ] = (
                    self.json_manager.main_widget.top_builder_widget.sequence_widget.button_frame.sequence_properties_manager.calculate_word()
                )
            if "author" not in sequence[0]:
                sequence[0][
                    "author"
                ] = (
                    self.json_manager.main_widget.main_window.settings_manager.users.user_manager.get_current_user()
                )
            if "level" not in sequence[0]:
                sequence[0]["level"] = (
                    self.json_manager.main_widget.sequence_level_evaluator.get_sequence_level(
                        sequence
                    )
                )
            if "prop_type" not in sequence[0]:
                sequence[0][
                    "prop_type"
                ] = self.json_manager.main_widget.prop_type.name.lower()
            if "is_circular" not in sequence[0]:
                sequence[0]["is_circular"] = False
            if "is_permutable" not in sequence[0]:
                sequence[0]["is_permutable"] = False

        # Add beat numbers to each beat at the beginning
        beat_number = 0
        for beat in sequence:
            if "letter" in beat or "sequence_start_position" in beat:
                beat_dict_with_beat_number = {"beat": beat_number}
                beat_dict_with_beat_number.update(beat)
                sequence[sequence.index(beat)] = beat_dict_with_beat_number
                beat_number += 1

        with open(self.current_sequence_json, "w", encoding="utf-8") as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

    def clear_current_sequence_file(self):
        self.save_current_sequence([])

    def get_prop_rot_dir_from_json(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[index][f"{color}_attributes"].get("prop_rot_dir", 0)
        return 0

    def get_motion_type_from_json_at_index(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[index][f"{color}_attributes"].get("motion_type", 0)
        return 0

    def get_prefloat_prop_rot_dir_from_json(self, index: int, color: str) -> int:
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(
                "prefloat_prop_rot_dir",
                sequence[index][f"{color}_attributes"].get("prop_rot_dir", 0),
            )
        return 0

    def get_prefloat_motion_type_from_json_at_index(
        self, index: int, color: str
    ) -> int:
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[index][f"{color}_attributes"].get(
                "prefloat_motion_type",
                sequence[index][f"{color}_attributes"].get("motion_type", 0),
            )
        return 0



    def get_red_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["red_attributes"]["end_ori"]
        return 0

    def get_blue_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["blue_attributes"]["end_ori"]
        return 0
