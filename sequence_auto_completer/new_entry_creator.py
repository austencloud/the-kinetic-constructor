from typing import TYPE_CHECKING, Dict

from data.constants import EAST, NORTH, SOUTH, WEST

if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter


class NewEntryCreator:
    def __init__(self, autocompleter: "SequenceAutoCompleter"):
        self.autocompleter = autocompleter

    def create_new_entry(
        self,
        sequence,
        previous_entry,
        last_position: str,
        beat_number: int,
        final_intended_sequence_length: int,
        halved_or_quartered,
    ) -> Dict:
        previous_matching_beat = self.get_previous_matching_beat(
            sequence, beat_number, final_intended_sequence_length, halved_or_quartered
        )

        previous_blue_end_ori = previous_entry["blue_attributes"]["end_ori"]
        previous_red_end_ori = previous_entry["red_attributes"]["end_ori"]
        previous_blue_end_loc = previous_entry["blue_attributes"]["end_loc"]
        previous_red_end_loc = previous_entry["red_attributes"]["end_loc"]

        new_entry = {
            "beat": beat_number,
            "letter": previous_matching_beat["letter"],
            "start_pos": last_position,
            "end_pos": self.calculate_new_end_pos(
                previous_matching_beat, previous_entry
            ),
            "timing": previous_matching_beat["timing"],
            "direction": previous_matching_beat["direction"],
            "blue_attributes": self.create_new_attributes(
                previous_blue_end_ori,
                previous_blue_end_loc,
                previous_matching_beat["blue_attributes"],
            ),
            "red_attributes": self.create_new_attributes(
                previous_red_end_ori,
                previous_red_end_loc,
                previous_matching_beat["red_attributes"],
            ),
        }

        new_entry["blue_attributes"]["end_ori"] = (
            self.autocompleter.json_manager.ori_calculator.calculate_end_orientation(
                new_entry, "blue"
            )
        )
        new_entry["red_attributes"]["end_ori"] = (
            self.autocompleter.json_manager.ori_calculator.calculate_end_orientation(
                new_entry, "red"
            )
        )

        return new_entry

    def calculate_new_end_pos(
        self, previous_matching_beat: dict, previous_entry: dict
    ) -> str:
        new_blue_end_loc = self.autocompleter.calculate_new_loc(
            previous_entry["blue_attributes"]["end_loc"],
            self.get_hand_rot_dir_from_locs(
                previous_matching_beat["blue_attributes"]["start_loc"],
                previous_matching_beat["blue_attributes"]["end_loc"],
            ),
        )
        new_red_end_loc = self.autocompleter.calculate_new_loc(
            previous_entry["red_attributes"]["end_loc"],
            self.get_hand_rot_dir_from_locs(
                previous_matching_beat["red_attributes"]["start_loc"],
                previous_matching_beat["red_attributes"]["end_loc"],
            ),
        )
        new_end_pos = self.get_numbered_position_from_locs(
            new_blue_end_loc, new_red_end_loc
        )
        return new_end_pos

    def get_hand_rot_dir_from_locs(self, start_loc: str, end_loc: str) -> str:
        hand_rot_dir_map = {
            (SOUTH, WEST): "cw",
            (WEST, NORTH): "cw",
            (NORTH, EAST): "cw",
            (EAST, SOUTH): "cw",
            (WEST, SOUTH): "ccw",
            (NORTH, WEST): "ccw",
            (EAST, NORTH): "ccw",
            (SOUTH, EAST): "ccw",
            (SOUTH, NORTH): "dash",
            (WEST, EAST): "dash",
            (NORTH, SOUTH): "dash",
            (EAST, WEST): "dash",
            (NORTH, NORTH): "static",
            (EAST, EAST): "static",
            (SOUTH, SOUTH): "static",
            (WEST, WEST): "static",
        }
        return hand_rot_dir_map.get((start_loc, end_loc))

    def get_numbered_position_from_locs(self, blue_loc: str, red_loc: str) -> str:
        positions_map: dict[tuple[str], str] = {
            (SOUTH, NORTH): "alpha1",
            (WEST, EAST): "alpha2",
            (NORTH, SOUTH): "alpha3",
            (EAST, WEST): "alpha4",
            (NORTH, NORTH): "beta1",
            (EAST, EAST): "beta2",
            (SOUTH, SOUTH): "beta3",
            (WEST, WEST): "beta4",
            (WEST, NORTH): "gamma1",
            (NORTH, EAST): "gamma2",
            (EAST, SOUTH): "gamma3",
            (SOUTH, WEST): "gamma4",
            (EAST, NORTH): "gamma5",
            (SOUTH, EAST): "gamma6",
            (WEST, SOUTH): "gamma7",
            (NORTH, WEST): "gamma8",
        }
        return positions_map.get((blue_loc, red_loc))

    def get_previous_matching_beat(
        self, sequence, beat_number, final_length, halved_or_quartered
    ) -> dict:
        if halved_or_quartered == "quartered":
            index_map = self.get_quartered_index_map()
        elif halved_or_quartered == "halved":
            index_map = self.get_halved_index_map()
        return sequence[index_map[final_length][beat_number]]

    def get_halved_index_map(self):
        index_map = {
            4: {3: 2, 4: 3},
            6: {4: 2, 5: 3, 6: 4},
            8: {5: 2, 6: 3, 7: 4, 8: 5},
            10: {6: 2, 7: 3, 8: 4, 9: 5, 10: 6},
            12: {7: 2, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7},
            14: {8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 14: 8},
            16: {
                9: 2,
                10: 3,
                11: 4,
                12: 5,
                13: 6,
                14: 7,
                15: 8,
                16: 9,
            },
            18: {
                10: 2,
                11: 3,
                12: 4,
                13: 5,
                14: 6,
                15: 7,
                16: 8,
                17: 9,
                18: 10,
            },
            20: {
                11: 2,
                12: 3,
                13: 4,
                14: 5,
                15: 6,
                16: 7,
                17: 8,
                18: 9,
                19: 10,
                20: 11,
            },
            22: {
                12: 2,
                13: 3,
                14: 4,
                15: 5,
                16: 6,
                17: 7,
                18: 8,
                19: 9,
                20: 10,
                21: 11,
                22: 12,
            },
            24: {
                13: 2,
                14: 3,
                15: 4,
                16: 5,
                17: 6,
                18: 7,
                19: 8,
                20: 9,
                21: 10,
                22: 11,
                23: 12,
                24: 13,
            },
        }

        return index_map

    def get_quartered_index_map(self):
        index_map = {
            4: {2: 2, 3: 3, 4: 4},
            8: {3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7},
            12: {4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10},
            16: {
                5: 2,
                6: 3,
                7: 4,
                8: 5,
                9: 6,
                10: 7,
                11: 8,
                12: 9,
                13: 10,
                14: 11,
                15: 12,
                16: 13,
            },
            20: {
                6: 2,
                7: 3,
                8: 4,
                9: 5,
                10: 6,
                11: 7,
                12: 8,
                13: 9,
                14: 10,
                15: 11,
                16: 12,
                17: 13,
                18: 14,
                19: 15,
                20: 16,
            },
            24: {
                6: 2,
                7: 3,
                8: 4,
                9: 5,
                10: 6,
                11: 7,
                12: 8,
                13: 9,
                14: 10,
                15: 11,
                16: 12,
                17: 13,
                18: 14,
                19: 15,
                20: 16,
                21: 17,
                22: 18,
                23: 19,
                24: 20,
            },
        }

        return index_map

    def create_new_attributes(
        self,
        previous_ori: str,
        previous_loc: str,
        previous_matching_beat_attributes: Dict,
    ) -> Dict:
        new_attributes = {
            "motion_type": previous_matching_beat_attributes["motion_type"],
            "start_ori": previous_ori,
            "prop_rot_dir": previous_matching_beat_attributes["prop_rot_dir"],
            "start_loc": previous_loc,
            "end_loc": self.autocompleter.calculate_new_loc(
                previous_loc,
                self.get_hand_rot_dir_from_locs(
                    previous_matching_beat_attributes["start_loc"],
                    previous_matching_beat_attributes["end_loc"],
                ),
            ),
            "turns": previous_matching_beat_attributes["turns"],
        }
        return new_attributes
