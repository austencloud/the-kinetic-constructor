from typing import Dict, List, Tuple
from df_generator import DataFrameGenerator
from constants import *
from Enums import *
from utilities.TypeChecking.Letters import *


class Type1Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type1_letters)
        self.create_Type1_dataframes()

    def create_Type1_dataframes(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

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
            for red_handpath_rot_dir in self.handpath_rot_dirs:
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

    def create_ST_dataframes(
        self,
        letter,
        red_motion_type,
        red_leading_bool,
    ):
        variations = []
        blue_motion_type = red_motion_type
        handpath_tuple_map_collection = self.get_handpath_tuple_map_collection()
        for handpath, values in handpath_tuple_map_collection.items():
            handpath_tuples = handpath_tuple_map_collection[handpath]
            for red_start_loc, red_end_loc in handpath_tuples:
                red_prop_rot_dir = self.get_prop_rot_dir(red_motion_type, handpath)
                blue_prop_rot_dir = red_prop_rot_dir

                blue_start_loc, blue_end_loc = self.determine_ST_start_end_loc(
                    red_start_loc, red_end_loc, red_prop_rot_dir, red_leading_bool
                )

                start_pos, end_pos = self.get_start_end_positions(
                    blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
                )

                variation = {
                    "letter": letter,
                    "start_position": start_pos,
                    "end_position": end_pos,
                    "blue_motion_type": blue_motion_type,
                    "blue_prop_rot_dir": blue_prop_rot_dir,
                    "blue_start_location": blue_start_loc,
                    "blue_end_location": blue_end_loc,
                    "red_motion_type": red_motion_type,
                    "red_prop_rot_dir": red_prop_rot_dir,
                    "red_start_location": red_start_loc,
                    "red_end_location": red_end_loc,
                }

                variations.append(variation)

        return variations

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        shift_handpath_tuple_map_collection = self.get_handpath_tuple_map_collection()

        for shift_handpath, values in shift_handpath_tuple_map_collection.items():
            red_prop_rot_dir = self.get_prop_rot_dir(red_motion_type, shift_handpath)
            blue_prop_rot_dir = (
                red_prop_rot_dir
                if letter in Type1_same_prop_rot_dir_letters
                else self.get_opposite_rot_dir(red_prop_rot_dir)
            )

            shift_handpath_tuples = shift_handpath_tuple_map_collection[shift_handpath]
            for red_start_loc, red_end_loc in shift_handpath_tuples:
                blue_start_loc, blue_end_loc = self.determine_blue_locations(
                    letter, red_start_loc, red_end_loc
                )

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )

                data.append(
                    {
                        "letter": letter,
                        "start_position": start_pos,
                        "end_position": end_pos,
                        "blue_motion_type": blue_motion_type,
                        "blue_prop_rot_dir": blue_prop_rot_dir,
                        "blue_start_loc": blue_start_loc,
                        "blue_end_loc": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_prop_rot_dir": red_prop_rot_dir,
                        "red_start_loc": red_start_loc,
                        "red_end_loc": red_end_loc,
                    }
                )

        return data

    def create_dataframes_for_U(self) -> List[Dict]:
        data = []
        red_pro_handpath_rot_dir = self.get_handpath_tuple_map_collection()

        for red_handpath_rot_dir in self.handpath_rot_dirs:
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
        red_pro_handpath_rot_dir = self.get_handpath_tuple_map_collection()

        for red_handpath_rot_dir in self.handpath_rot_dirs:
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
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
                        self.create_variation_dict(
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

    def create_variation_dict(
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
        start_pos, end_pos = self.get_start_end_positions(
            blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
        )
        return {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": blue_motion_type,
            "blue_prop_rot_dir": blue_prop_rot_dir,
            "blue_start_location": blue_start_loc,
            "blue_end_location": blue_end_loc,
            "red_motion_type": red_motion_type,
            "red_prop_rot_dir": red_prop_rot_dir,
            "red_start_location": red_start_loc,
            "red_end_location": red_end_loc,
        }

    def determine_blue_locations(
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
