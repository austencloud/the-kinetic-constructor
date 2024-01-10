from typing import Dict, List

import pandas as pd
from utilities.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)
from constants import *
from utilities.TypeChecking.Letters import *


class Type1Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type1_letters)
        self.create_Type1_dataframes()

    def create_Type1_dataframes(self) -> pd.DataFrame:
        all_data = []
        for letter in self.letters:
            data = self.create_dataframe(letter)
            all_data.extend(data)
            print("Generated dataframes for letter:", letter)
        return pd.DataFrame(all_data)

    def create_dataframe(self, letter) -> List[Dict]:
        data = []
        if letter in ["A", "D", "G", "J", "M", "P", "M", "P"]:
            return self.create_dataframes_for_letter(letter, PRO, PRO)
        elif letter in ["B", "E", "H", "K", "N", "Q", "N", "Q"]:
            return self.create_dataframes_for_letter(letter, ANTI, ANTI)
        elif letter in ["C", "F", "I", "L", "O", "R"]:
            data = self.create_dataframes_for_letter(letter, PRO, ANTI)
            data += self.create_dataframes_for_letter(letter, ANTI, PRO)

        if letter in ["S", "T"]:
            red_motion_type = PRO if letter == "S" else ANTI
            for red_handpath_rot_dir in self.shift_handpaths:
                data: List = self.create_ST_dataframes(
                    letter,
                    red_motion_type,
                    red_leading_bool=True,
                )
                data.extend(
                    self.create_ST_dataframes(
                        letter,
                        red_motion_type,
                        red_leading_bool=False,
                    )
                )
        elif letter == "U":
            return self.create_dataframes_for_U()
        elif letter == "V":
            return self.create_dataframes_for_V()
        return data

    ### ABCDEFGHIJKLMNOPQR ###

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []

        for shift_handpath in self.shift_handpaths:
            shift_handpath_tuple_map_collection = (
                self.get_shift_tuple_map_from_handpath(shift_handpath)
            )
            red_prop_rot_dir = self.get_prop_rot_dir(red_motion_type, shift_handpath)
            blue_prop_rot_dir = (
                red_prop_rot_dir
                if letter in Type1_same_prop_rot_dir_letters
                else self.get_opposite_rot_dir(red_prop_rot_dir)
            )

            shift_handpath_tuples = shift_handpath_tuple_map_collection
            for red_start_loc, red_end_loc in shift_handpath_tuples:
                blue_start_loc, blue_end_loc = self.get_blue_locations(
                    letter, red_start_loc, red_end_loc
                )

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

    ### STUV ###

    def create_ST_dataframes(
        self,
        letter,
        red_motion_type,
        red_leading_bool,
    ):
        variations = []
        blue_motion_type = red_motion_type
        for shift_handpath in self.shift_handpaths:
            shift_tuple_map = self.get_shift_tuple_map_from_handpath(shift_handpath)
            for red_start_loc, red_end_loc in shift_tuple_map:
                red_prop_rot_dir = self.get_prop_rot_dir(
                    red_motion_type, shift_handpath
                )
                blue_prop_rot_dir = red_prop_rot_dir

                blue_start_loc, blue_end_loc = self.determine_ST_start_end_loc(
                    red_start_loc, red_end_loc, red_prop_rot_dir, red_leading_bool
                )

                start_pos, end_pos = self.get_start_end_poss(
                    blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
                )

                variation = {
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

                variations.append(variation)

        return variations

    def create_dataframes_for_U(self) -> List[Dict]:
        data = []

        for red_handpath_rot_dir in self.shift_handpaths:
            shift_tuple_map = self.get_shift_tuple_map_from_handpath(
                red_handpath_rot_dir
            )
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_U_V_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Blue leading with CW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_U_V_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_U_V_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_U_V_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

        return data

    def create_dataframes_for_V(self) -> List[Dict]:
        data = []

        for red_handpath_rot_dir in self.shift_handpaths:
            shift_tuple_map = self.get_shift_tuple_map_from_handpath(
                red_handpath_rot_dir
            )
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_U_V_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Blue leading with CW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_U_V_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_U_V_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CW_HANDPATH
            for red_start_loc, red_end_loc in shift_tuple_map:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_U_V_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

        return data

    ### HELPERS ###

    def determine_ST_start_end_loc(
        self, red_start_loc, red_end_loc, red_prop_rot_dir, red_leading
    ):
        if red_leading:
            # If red is leading, then blue follows red's starting location,
            # and blue's end location is where red started from.
            blue_start_loc = self.get_opposite_location(red_end_loc)
            blue_end_loc = red_start_loc
        else:
            # If blue is leading, then blue's start location is where red ended,
            # and blue's end location is the opposite of where red started from.
            blue_start_loc = red_end_loc
            blue_end_loc = self.get_opposite_location(red_start_loc)

        return blue_start_loc, blue_end_loc

    def create_U_V_variation_dict(
        self,
        letter,
        red_start_loc,
        red_end_loc,
        blue_start_loc,
        blue_end_loc,
        red_motion_type,
        red_prop_rot_dir,
        blue_motion_type,
        blue_prop_rot_dir,
    ):
        start_pos, end_pos = self.get_start_end_poss(
            blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
        )
        return {
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

    def get_blue_locations(
        self, letter, red_start_loc, red_end_loc, red_leading_bool=None
    ):
        if letter in Type1_alpha_to_alpha_letters:  # A, B, C
            blue_start_loc = self.get_opposite_location(red_start_loc)
            blue_end_loc = self.get_opposite_location(red_end_loc)
        elif letter in Type1_beta_to_alpha_letters:  # D, E, F
            blue_start_loc = red_start_loc
            blue_end_loc = self.get_opposite_location(red_end_loc)
        elif letter in Type1_beta_to_beta_letters:  # G, H, I
            blue_start_loc, blue_end_loc = red_start_loc, red_end_loc
        elif letter in Type1_alpha_to_beta_letters:  # J, K, L
            blue_start_loc = self.get_opposite_location(red_start_loc)
            blue_end_loc = red_end_loc
        elif letter in Type1_gamma_opp_parallel_letters:  # M, N, O
            blue_start_loc = self.get_opposite_location(red_end_loc)
            blue_end_loc = self.get_opposite_location(red_start_loc)
        elif letter in Type1_gamma_opp_antiparallel_letters:  # P, Q, R
            blue_start_loc = red_end_loc
            blue_end_loc = red_start_loc
        elif letter in Type1_gamma_same_dir_letters:  # S, T, U, V
            if red_leading_bool:
                blue_start_loc = self.get_opposite_location(red_end_loc)
                blue_end_loc = red_start_loc
            elif not red_leading_bool:
                blue_start_loc = red_end_loc
                blue_end_loc = self.get_opposite_location(red_start_loc)
        return blue_start_loc, blue_end_loc


# Instantiate and run the generator
alpha_beta_generator = Type1Generator()
