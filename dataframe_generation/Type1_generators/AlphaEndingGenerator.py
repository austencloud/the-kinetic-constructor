from typing import Dict, List
from df_generator import DataFrameGenerator
from data.constants import *


class AlphaEndingGenerator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["A", "B", "C", "D", "E", "F"])
        self.alpha_to_alpha_letters = ["A", "B", "C"]
        self.beta_to_alpha_letters = ["D", "E", "F"]
        self.create_dataframes_for_alpha_ending()

    def create_dataframes_for_alpha_ending(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        # For A and D, only 'pro' motion types are considered.
        if letter in ["A", "D"]:
            return self.create_dataframes_for_letter(letter, "pro", "pro")
        # For B and E, only 'anti' motion types are considered.
        elif letter in ["B", "E"]:
            return self.create_dataframes_for_letter(letter, "anti", "anti")
        # For C and F, both 'pro-anti' and 'anti-pro' combinations are considered.
        elif letter in ["C", "F"]:
            data = self.create_dataframes_for_letter(letter, "pro", "anti")
            data += self.create_dataframes_for_letter(letter, "anti", "pro")
            return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        handpath_tuple_map_collection = self.get_handpath_tuple_map_collection(
            red_motion_type
        )

        for handpath, handpath_tuples in handpath_tuple_map_collection.items():
            red_prop_rot_dir = self.get_red_prop_rot_dir(red_motion_type, handpath)

            for red_start_loc, red_end_loc in handpath_tuples:
                blue_prop_rot_dir = (
                    self.get_opposite_rot_dir(red_prop_rot_dir)
                    if letter
                    in [
                        "C",
                        "D",
                        "E",
                    ]  # These letters have props rotating in opposite directions
                    else red_prop_rot_dir
                )

                if letter in self.alpha_to_alpha_letters:
                    blue_loc_pair = self.get_opposite_loc_tuple(
                        (red_start_loc, red_end_loc)
                    )
                    blue_start_loc, blue_end_loc = blue_loc_pair
                elif letter in self.beta_to_alpha_letters:
                    blue_start_loc = red_start_loc
                    blue_end_loc = self.get_opposite_location(red_end_loc)

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )

                # Append the data dictionary
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


# Instantiate and run the generator
alpha_ending_generator = AlphaEndingGenerator()
