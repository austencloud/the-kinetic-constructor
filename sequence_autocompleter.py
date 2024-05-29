from typing import TYPE_CHECKING, List, Dict
from position_maps import position_map_cw, position_map_ccw

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SequenceAutocompleter:
    def __init__(self, beat_frame: "SW_BeatFrame"):
        self.json_handler = beat_frame.current_sequence_json_manager
        self.beat_frame = beat_frame

    def perform_auto_completion(self, sequence: List[Dict]):
        # Identify the starting position entry
        start_position_entry = (
            sequence[0] if "sequence_start_position" in sequence[0] else None
        )

        if start_position_entry:
            sequence = sequence[1:]  # Exclude the start position entry for copying

        last_position = sequence[-1]["end_pos"]
        direction = self.get_rotation_direction(sequence)

        new_entries = []
        for i, entry in enumerate(sequence):
            if "prop_type" in entry or "sequence_start_position" in entry:
                continue  # Skip non-pictograph entries

            new_entry = entry.copy()
            new_entry["beat"] = i + 1  # Add beat number at the beginning
            new_entry["start_pos"] = last_position
            new_entry["end_pos"] = self.calculate_new_end_pos(last_position, direction)

            # Update attributes based on the previous entry's end state
            new_entry = self.update_attributes(new_entry, entry)

            last_position = new_entry["end_pos"]
            new_entries.append(new_entry)

        if start_position_entry:
            start_position_entry["beat"] = 0
            sequence.insert(0, start_position_entry)

        sequence.extend(new_entries)
        self.json_handler.save_current_sequence(sequence)

    def get_rotation_direction(self, sequence: List[Dict]) -> str:
        for entry in sequence:
            if (
                "blue_attributes" in entry
                and "prop_rot_dir" in entry["blue_attributes"]
            ):
                return entry["blue_attributes"]["prop_rot_dir"]
            elif (
                "red_attributes" in entry and "prop_rot_dir" in entry["red_attributes"]
            ):
                return entry["red_attributes"]["prop_rot_dir"]
        return "cw"  # Default to clockwise if not specified

    def calculate_new_end_pos(self, last_position: str, direction: str) -> str:
        pos_map = position_map_cw if direction == "cw" else position_map_ccw
        return pos_map.get(last_position, "alpha1")

    def update_attributes(self, new_entry: Dict, previous_entry: Dict) -> Dict:
        # Ensure the new entry's attributes are consistent with the previous entry's end state
        new_entry["blue_attributes"]["start_loc"] = previous_entry["blue_attributes"][
            "end_loc"
        ]
        new_entry["blue_attributes"]["start_ori"] = previous_entry["blue_attributes"][
            "end_ori"
        ]
        new_entry["red_attributes"]["start_loc"] = previous_entry["red_attributes"][
            "end_loc"
        ]
        new_entry["red_attributes"]["start_ori"] = previous_entry["red_attributes"][
            "end_ori"
        ]

        # Calculate the new end locations based on the start positions and the type of motion
        new_entry["blue_attributes"]["end_loc"] = self.calculate_new_loc(
            new_entry["blue_attributes"]["start_loc"],
            new_entry["blue_attributes"]["prop_rot_dir"],
            new_entry["blue_attributes"]["motion_type"],
        )
        new_entry["red_attributes"]["end_loc"] = self.calculate_new_loc(
            new_entry["red_attributes"]["start_loc"],
            new_entry["red_attributes"]["prop_rot_dir"],
            new_entry["red_attributes"]["motion_type"],
        )

        return new_entry

    def calculate_new_loc(
        self, start_loc: str, prop_rot_dir: str, motion_type: str
    ) -> str:
        if motion_type == "pro":
            if prop_rot_dir == "cw":
                loc_map = {"s": "w", "w": "n", "n": "e", "e": "s"}
            else:  # ccw
                loc_map = {"s": "e", "e": "n", "n": "w", "w": "s"}
        else:  # static
            loc_map = {loc: loc for loc in ["s", "w", "n", "e"]}

        return loc_map.get(start_loc, "s")
