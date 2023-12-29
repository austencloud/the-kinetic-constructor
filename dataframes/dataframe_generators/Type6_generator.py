from typing import Dict, List, Tuple

import pandas as pd
from dataframes.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)
from Enums import Location
from constants import *
from utilities.TypeChecking.Letters import Type6_letters


class Type6Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type6_letters)
        self.create_Type6_dataframes()

    def create_Type6_dataframes(self) -> pd.DataFrame:
        all_data = []
        for letter in self.letters:
            data = self.create_dataframe(letter)
            all_data.extend(data)
            print("Generated dataframes for letter:", letter)
        return pd.DataFrame(all_data)

    def create_dataframe(self, letter) -> List[Dict]:
        data = []
        if letter == "Γ":
            data = self.create_dataframes_for_Γ(letter)
        else:  # α or β
            data += self.create_dataframes_for_letter(letter, STATIC, STATIC)
        return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        static_tuple_map = self.get_static_tuple_map()
        red_prop_rot_dir = "NoRotation"
        blue_prop_rot_dir = "NoRotation"
        for red_start_loc, red_end_loc in static_tuple_map:
            blue_start_loc, blue_end_loc = self.get_blue_locations(
                letter, red_start_loc, red_end_loc
            )
            start_pos, end_pos = self.get_Type1_start_and_end_pos(
                red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
            )
            data.append(
                {
                    "letter": letter,
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                    BLUE_MOTION_TYPE: blue_motion_type,
                    "blue_prop_rot_dir": blue_prop_rot_dir,
                    "blue_start_loc": blue_start_loc,
                    "blue_end_loc": blue_end_loc,
                    RED_MOTION_TYPE: red_motion_type,
                    "red_prop_rot_dir": red_prop_rot_dir,
                    "red_start_loc": red_start_loc,
                    "red_end_loc": red_end_loc,
                }
            )
        return data

    def create_dataframes_for_Γ(self, letter) -> List[Dict]:
        data = []
        static_tuple_map = self.get_static_tuple_map()
        for red_start_loc, red_end_loc in static_tuple_map:
            data += self.create_Λ_variations(letter, red_start_loc, red_end_loc)
        return data

    def create_Λ_variations(self, letter, red_start_loc, red_end_loc) -> List[Dict]:
        variations = []
        blue_loc_tuples = self.get_blue_loc_tuples_for_Λ_dash(
            red_start_loc, red_end_loc
        )

        for blue_start_loc, blue_end_loc in blue_loc_tuples:
            variations.append(
                self.create_variation_dict(
                    letter,
                    blue_start_loc,
                    blue_end_loc,
                    red_start_loc,
                    red_end_loc,
                    STATIC,
                    STATIC,
                )
            )

        return variations

    def get_blue_loc_tuples_for_Λ_dash(
        self, red_start_loc, red_end_loc
    ) -> List[Tuple[Location, Location]]:
        blue_location_map = {
            (NORTH, NORTH): [(EAST, EAST), (WEST, WEST)],
            (EAST, EAST): [(SOUTH, SOUTH), (NORTH, NORTH)],
            (SOUTH, SOUTH): [(WEST, WEST), (EAST, EAST)],
            (WEST, WEST): [(NORTH, NORTH), (SOUTH, SOUTH)],
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
    ) -> Dict:
        start_pos, end_pos = self.get_Type1_start_and_end_pos(
            red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
        )
        return {
            "letter": letter,
            "start_pos": start_pos,
            "end_pos": end_pos,
            BLUE_MOTION_TYPE: blue_motion_type,
            "blue_prop_rot_dir": "NoRotation",
            "blue_start_loc": blue_start_loc,
            "blue_end_loc": blue_end_loc,
            RED_MOTION_TYPE: red_motion_type,
            "red_prop_rot_dir": "NoRotation",
            "red_start_loc": red_start_loc,
            "red_end_loc": red_end_loc,
        }

    def get_blue_locations(
        self, letter, red_start_loc, red_end_loc
    ) -> Tuple[Location, Location]:
        if letter == "α":
            blue_start_loc, blue_end_loc = self.get_opposite_loc_tuple(
                (red_start_loc, red_end_loc)
            )
        elif letter == "β":
            blue_start_loc, blue_end_loc = red_start_loc, red_end_loc
        return blue_start_loc, blue_end_loc


Type6Generator()
