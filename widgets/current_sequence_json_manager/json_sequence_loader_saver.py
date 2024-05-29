import json
from typing import TYPE_CHECKING, List, Dict
from path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from widgets.current_sequence_json_manager.current_sequence_json_manager import (
        CurrentSequenceJsonManager,
    )


class JsonSequenceLoaderSaver:
    def __init__(self, manager: "CurrentSequenceJsonManager"):
        self.manager = manager
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
                    "prop_type": self.manager.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                }
            ]

    def save_current_sequence(self, sequence: List[Dict]):
        if not sequence:
            sequence = [
                {
                    "prop_type": self.manager.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                }
            ]
        else:
            if "prop_type" not in sequence[0]:
                sequence[0][
                    "prop_type"
                ] = self.manager.main_widget.prop_type.name.lower()
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
