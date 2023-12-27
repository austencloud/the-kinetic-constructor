from typing import Dict, List
from df_generator import DataFrameGenerator
from data.constants import *


class DEF_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["D", "E", "F"])
        self.create_dataframes_for_DEF()

    def create_dataframes_for_DEF(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter == "D":
            return self.create_dataframes_for_letter("D", "pro", "pro")
        elif letter == "E":
            return self.create_dataframes_for_letter("E", "anti", "anti")
        elif letter == "F":
            # For "F", generate "pro"-"anti" and "anti"-"pro" combinations without causing recursion
            data = self.create_dataframes_for_letter("F", "pro", "anti")
            data += self.create_dataframes_for_letter("F", "anti", "pro")
            return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        self.handpath_tuple_map_collection = self.get_handpath_tuple_map_collection(
            red_motion_type
        )

        # Ensure that self.handpath_tuple_map_collection is a list of tuples
        self.handpath_tuple_map_collection = list(
            self.handpath_tuple_map_collection.items()
        )
        for red_handpath, red_handpath_tuples in self.handpath_tuple_map_collection:
            if red_handpath == CW_HANDPATH:
                if red_motion_type == PRO:
                    red_handpath_rot_dir = CW_HANDPATH
                elif red_motion_type == ANTI:
                    red_handpath_rot_dir = CCW_HANDPATH
            elif red_handpath == CCW_HANDPATH:
                if red_motion_type == PRO:
                    red_handpath_rot_dir = CCW_HANDPATH
                elif red_motion_type == ANTI:
                    red_handpath_rot_dir = CW_HANDPATH

            red_prop_rot_dir = self.get_red_prop_rot_dir(
                red_motion_type, red_handpath_rot_dir
            )

            for red_start_loc, red_end_loc in red_handpath_tuples:
                if self.is_hybrid(letter):
                    blue_prop_rot_dir = red_prop_rot_dir
                else:
                    blue_prop_rot_dir = self.get_opposite_rot_dir(red_prop_rot_dir)

                blue_start_loc = red_start_loc
                blue_end_loc = self.get_opposite_location(red_end_loc)

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
                        "blue_start_location": blue_start_loc,
                        "blue_end_location": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_rot_dir": red_prop_rot_dir,
                        "red_start_location": red_start_loc,
                        "red_end_location": red_end_loc,
                    }
                )
        return data


DEF_Generator()
