from typing import Dict, List, Tuple

import pandas as pd
from dataframes.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)
from Enums import Location
from constants import *
from utilities.TypeChecking.Letters import Type5_letters


class Type5Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type5_letters)
        self.create_Type5_dataframes()

    def create_Type5_dataframes(self) -> pd.DataFrame:
        all_data = []
        for letter in self.letters:
            data = self.create_dataframe(letter)
            all_data.extend(data)
            print("Generated dataframes for letter:", letter)
        return pd.DataFrame(all_data)

    def create_dataframe(self, letter) -> List[Dict]:
        data = []
        if letter == "Λ-":
            data = self.create_dataframes_for_Λ_dash(letter)
        else:
            data += self.create_dataframes_for_letter(letter, DASH, DASH)
        return data

    def create_dataframes_for_letter(self, letter, red_motion_type, blue_motion_type):
        data = []
        dash_handpath_tuple_map = self.get_dash_tuple_map()
        red_prop_rot_dir = "NoRotation"
        blue_prop_rot_dir = "NoRotation"
        for start_loc, end_loc in dash_handpath_tuple_map:
            blue_start_loc, blue_end_loc = self.get_blue_locations(
                letter, start_loc, end_loc
            )
            red_start_loc, red_end_loc = start_loc, end_loc
            start_pos, end_pos = self.get_Type1_start_and_end_pos(
                red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
            )
            data.append(
                {
                    LETTER: letter,
                    START_POS: start_pos,
                    END_POS: end_pos,
                    BLUE_MOTION_TYPE: blue_motion_type,
                    BLUE_PROP_ROT_DIR: blue_prop_rot_dir,
                    BLUE_START_LOC: blue_start_loc,
                    BLUE_END_LOC: blue_end_loc,
                    RED_MOTION_TYPE: red_motion_type,
                    RED_PROP_ROT_DIR: red_prop_rot_dir,
                    RED_START_LOC: red_start_loc,
                    RED_END_LOC: red_end_loc,
                }
            )
        return data

    def create_dataframes_for_Λ_dash(self, letter):
        data = []
        # Λ specific logic for dash and static hand locations
        dash_handpath_tuple_map = self.get_dash_tuple_map()
        for red_start_loc, red_end_loc in dash_handpath_tuple_map:
            # Create variations where dash and static hands are at different locations
            data += self.create_Λ_variations(letter, red_start_loc, red_end_loc)
        return data

    def create_Λ_variations(self, letter, red_start_loc, red_end_loc):
        variations = []
        blue_loc_tuples = self.get_blue_loc_tuples_for_Λ_dash(
            red_start_loc, red_end_loc
        )

        for blue_start_loc, blue_end_loc in blue_loc_tuples:
            # Dash motion variations
            variations.append(
                self.create_variation_dict(
                    letter,
                    blue_start_loc,
                    blue_end_loc,
                    red_start_loc,
                    red_end_loc,
                    DASH,
                    DASH,
                )
            )

        return variations

    def get_blue_loc_tuples_for_Λ_dash(self, red_start_loc, red_end_loc) -> List[str]:
        """Gets valid dash tuples for Λ based on dash's start and end locs."""
        blue_location_map = {
            (NORTH, SOUTH): [(EAST, WEST), (WEST, EAST)],
            (EAST, WEST): [(NORTH, SOUTH), (SOUTH, NORTH)],
            (SOUTH, NORTH): [(EAST, WEST), (WEST, EAST)],
            (WEST, EAST): [(NORTH, SOUTH), (SOUTH, NORTH)],
        }
        return blue_location_map.get((red_start_loc, red_end_loc), [])

    def create_variation_dict(
        self,
        letter,
        blue_start_loc,
        blue_end_loc,
        red_start_loc,
        red_end_loc,
        red_motion_type,
        blue_motion_type,
    ):
        start_pos, end_pos = self.get_Type1_start_and_end_pos(
            red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
        )
        return {
            LETTER: letter,
            START_POS: start_pos,
            END_POS: end_pos,
            BLUE_MOTION_TYPE: blue_motion_type,
            BLUE_PROP_ROT_DIR: "NoRotation",
            BLUE_START_LOC: blue_start_loc,
            BLUE_END_LOC: blue_end_loc,
            RED_MOTION_TYPE: red_motion_type,
            RED_PROP_ROT_DIR: "NoRotation",
            RED_START_LOC: red_start_loc,
            RED_END_LOC: red_end_loc,
        }

    def get_blue_locations(
        self, letter, red_start_loc, red_end_loc
    ) -> Tuple[Location, Location]:
        if letter == "Φ-":
            blue_start_loc, blue_end_loc = red_end_loc, red_start_loc
        elif letter == "Ψ-":
            blue_start_loc, blue_end_loc = red_start_loc, red_end_loc
        return blue_start_loc, blue_end_loc


Type5Generator()
