from typing import Dict, List
from df_generator import DataFrameGenerator
from data.constants import *
from data.Enums import *


class AlphaBetaGenerator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type1_alpha_beta_letters)
        self.create_dataframes_for_alpha_beta()

    def create_dataframes_for_alpha_beta(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter in Type1_pro_letters:
            return self.create_dataframes_for_letter(letter, PRO, PRO)
        elif letter in Type1_anti_letters:
            return self.create_dataframes_for_letter(letter, ANTI, ANTI)
        elif letter in Type1_hybrid_letters:
            data = self.create_dataframes_for_letter(letter, PRO, ANTI)
            data += self.create_dataframes_for_letter(letter, ANTI, PRO)
            return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        handpath_tuple_map_collection = self.get_handpath_tuple_map_collection()

        for handpath, values in handpath_tuple_map_collection.items():
            red_prop_rot_dir = self.get_prop_rot_dir(red_motion_type, handpath)
            blue_prop_rot_dir = (
                red_prop_rot_dir
                if letter in Type1_same_prop_rot_dir_letters
                else self.get_opposite_rot_dir(red_prop_rot_dir)
            )

            handpath_tuples = handpath_tuple_map_collection[handpath]
            for red_start_loc, red_end_loc in handpath_tuples:
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
                        "blue_rot_dir": blue_prop_rot_dir,
                        "blue_start_loc": blue_start_loc,
                        "blue_end_loc": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_rot_dir": red_prop_rot_dir,
                        "red_start_loc": red_start_loc,
                        "red_end_loc": red_end_loc,
                    }
                )

        return data

    def determine_blue_locations(self, letter, red_start_loc, red_end_loc):
        if letter in alpha_to_alpha_letters:
            blue_start_loc = self.get_opposite_location(red_start_loc)
            blue_end_loc = self.get_opposite_location(red_end_loc)
        elif letter in beta_to_alpha_letters:
            blue_start_loc = red_start_loc
            blue_end_loc = self.get_opposite_location(red_end_loc)
        elif letter in beta_to_beta_letters:
            blue_start_loc, blue_end_loc = red_start_loc, red_end_loc
        elif letter in alpha_to_beta_letters:
            blue_start_loc = self.get_opposite_location(red_start_loc)
            blue_end_loc = red_end_loc
        return blue_start_loc, blue_end_loc



# Instantiate and run the generator
alpha_beta_generator = AlphaBetaGenerator()
