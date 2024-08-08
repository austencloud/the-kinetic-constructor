from typing import TYPE_CHECKING, List, Dict
from data.position_maps import position_map_cw, position_map_ccw
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from sequence_auto_completer.new_entry_creator import NewEntryCreator

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SequenceAutoCompleter:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.beat_frame = sequence_widget.beat_frame
        self.json_manager = self.beat_frame.json_manager
        self.new_entry_creator = NewEntryCreator(self)

    def perform_auto_completion(self, sequence: List[Dict]):
        start_position_entry = (
            sequence[0] if "sequence_start_position" in sequence[0] else None
        )

        if start_position_entry:
            sequence = sequence[1:]

        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        last_position = last_entry["end_pos"]
        permutation_rot_dir = self.get_permutation_rot_dir(sequence)

        new_entries = []
        next_beat_number = last_entry["beat"] + 1

        # if it's a halved permutation, set halved_or_quartered to "halved"
        # if it's a quartered permutation, set halved_or_quartered to "quartered"
        
        if self.is_halved_permutation():
            halved_or_quartered = "halved"
        elif self.is_quartered_permutation():
            halved_or_quartered = "quartered"

        if self.is_circular_sequence(sequence):
            entries_to_add = sequence_length * 3
            new_entries = self.create_circular_entries(
                sequence,
                entries_to_add,
                last_entry,
                permutation_rot_dir,
                next_beat_number,
            )
        else:
            entries_to_add = self.determine_how_many_entries_to_add(sequence_length)
            for _ in range(entries_to_add):
                new_entry = self.new_entry_creator.create_new_entry(
                    sequence,
                    last_entry,
                    last_position,
                    next_beat_number,
                    sequence_length + entries_to_add,
                    halved_or_quartered,
                )
                new_entries.append(new_entry)
                sequence.append(new_entry)
                last_entry = new_entry
                last_position = new_entry["end_pos"]
                next_beat_number += 1

        if start_position_entry:
            start_position_entry["beat"] = 0
            sequence.insert(0, start_position_entry)

        self.json_manager.loader_saver.save_current_sequence(sequence)
        self.beat_frame.populate_beat_frame_from_json(sequence)

    def is_circular_sequence(self, sequence: List[Dict]) -> bool:
        return sequence[0].get("is_circular", False)

    def create_circular_entries(
        self, sequence, entries_to_add, last_entry, direction, next_beat_number
    ):
        circular_entries = []
        original_sequence = sequence.copy()
        for _ in range(entries_to_add):
            for entry in original_sequence:
                if entry.get("beat") != 0:
                    new_entry = self.new_entry_creator.create_new_entry(
                        sequence,
                        last_entry,
                        last_entry["end_pos"],
                        next_beat_number,
                        len(sequence) + entries_to_add,
                    )
                    circular_entries.append(new_entry)
                    last_entry = new_entry
                    next_beat_number += 1
        return circular_entries

    def determine_how_many_entries_to_add(self, sequence_length: int) -> int:
        if self.is_quartered_permutation():
            return sequence_length * 3
        elif self.is_halved_permutation():
            return sequence_length
        return 0

    def is_quartered_permutation(self) -> bool:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        return (start_pos, end_pos) in quartered_permutations

    def is_halved_permutation(self) -> bool:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        return (start_pos, end_pos) in halved_permutations

    def get_permutation_rot_dir(self, sequence: List[Dict]) -> str:
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        if (start_pos, end_pos) in position_map_cw.items():
            return "cw"
        return "ccw"

    def calculate_new_end_pos(self, last_position: str, direction: str) -> str:
        pos_map = position_map_cw if direction == "cw" else position_map_ccw
        return pos_map.get(last_position, "alpha1")

    def calculate_new_loc(
        self, start_loc: str, hand_rot_dir: str
    ) -> str:
        loc_map_cw = {"s": "w", "w": "n", "n": "e", "e": "s"}
        loc_map_ccw = {"s": "e", "e": "n", "n": "w", "w": "s"}

        loc_map = loc_map_cw if hand_rot_dir == "cw" else loc_map_ccw

        if hand_rot_dir == "dash":
            loc_map = {"s": "n", "n": "s", "w": "e", "e": "w"}
        elif hand_rot_dir == "static":
            loc_map = {"s": "s", "n": "n", "w": "w", "e": "e"}

        return loc_map[start_loc]
