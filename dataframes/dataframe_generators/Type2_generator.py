from typing import Dict, List, Tuple
from dataframes.dataframe_generators.base_dataframe_generator import (
    BaseDataFrameGenerator,
)
from Enums import Location
from constants import *
from utilities.TypeChecking.Letters import Type2_letters


class Type2Generator(BaseDataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(Type2_letters)
        self.create_Type2_dataframes()

    def create_Type2_dataframes(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            print("Generated dataframes for letter:", letter)
            self.save_dataframe(letter, data, "Type_2")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter in ["W", "Y", "Σ", "θ"]:
            data = self.create_dataframes_for_letter(letter, PRO, STATIC)
            data += self.create_dataframes_for_letter(letter, STATIC, PRO)
        else:  # letter in ["X", "Z", "Δ", "Ω"]
            data = self.create_dataframes_for_letter(letter, ANTI, STATIC)
            data += self.create_dataframes_for_letter(letter, STATIC, ANTI)
        return data

    def create_dataframes_for_letter(self, letter, red_motion_type, blue_motion_type):
        data = []
        for shift_handpath in self.shift_handpaths:
            shift_tuple_map = self.get_shift_tuple_map_from_handpath(shift_handpath)
            for start_loc, end_loc in shift_tuple_map:
                if red_motion_type in [PRO, ANTI]:
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, shift_handpath
                    )
                else:
                    red_prop_rot_dir = "None"  # Explicitly indicating no rotation

                if blue_motion_type in [PRO, ANTI]:
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, shift_handpath
                    )
                else:
                    blue_prop_rot_dir = "None"  # Explicitly indicating no rotation

                if red_motion_type == STATIC:
                    red_start_loc, red_end_loc = self.get_static_locations(
                        letter, start_loc, end_loc
                    )
                    blue_start_loc, blue_end_loc = start_loc, end_loc
                elif blue_motion_type == STATIC:
                    blue_start_loc, blue_end_loc = self.get_static_locations(
                        letter, start_loc, end_loc
                    )
                    red_start_loc, red_end_loc = start_loc, end_loc
                else:
                    red_start_loc, red_end_loc = start_loc, end_loc
                    blue_start_loc, blue_end_loc = start_loc, end_loc

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

    def get_static_locations(
        self, letter, shift_start_loc, shift_end_loc
    ) -> Tuple[Location, Location]:
        if letter in ["W", "X"]:  # Static starts at shift_end_loc
            static_start_loc, static_end_loc = self.get_opposite_location(
                shift_end_loc
            ), self.get_opposite_location(shift_end_loc)
        elif letter in ["Y", "Z"]:  # Static ends at shift_end_loc
            static_start_loc, static_end_loc = shift_end_loc, shift_end_loc
        elif letter in ["θ", "Ω"]:  # Static ends at shift_start_loc
            static_start_loc, static_end_loc = shift_start_loc, shift_start_loc
        elif letter in ["Σ", "Δ"]:  # Static starts at shift_start_loc
            static_start_loc, static_end_loc = self.get_opposite_location(
                shift_start_loc
            ), self.get_opposite_location(shift_start_loc)
        return static_start_loc, static_end_loc


Type2Generator()
