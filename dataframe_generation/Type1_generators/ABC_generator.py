from typing import Dict, List, Tuple
from data.Enums import Location, RotationDirection
from df_generator import DataFrameGenerator


class ABC_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["A", "B", "C"])
        self.create_dataframes_for_ABC()

    def create_dataframes_for_ABC(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter == "A":
            return self.create_dataframe_for_A()
        elif letter == "B":
            return self.create_dataframe_for_B()
        elif letter == "C":
            return self.create_dataframe_for_C()

    def create_dataframe_for_A(self) -> List[Dict]:
        return self.create_dataframes_for_letter("A", "pro", "pro")

    def create_dataframe_for_B(self) -> List[Dict]:
        return self.create_dataframes_for_letter("B", "anti", "anti")

    def create_dataframe_for_C(self) -> List[Dict]:
        data = self.create_dataframes_for_letter("C", "pro", "anti")
        data.extend(self.create_dataframes_for_letter("C", "anti", "pro"))
        return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        for red_rot_dir in self.rotation_directions:
            red_shifts = self.define_shifts(red_motion_type)[red_rot_dir]
            for red_loc_pair in red_shifts:
                red_start_loc, red_end_loc = red_loc_pair
                blue_rot_dir = self.get_opposite_rot_dir(red_rot_dir)
                blue_loc_pair = self.get_opposite_shifts(red_loc_pair)
                blue_start_loc, blue_end_loc = blue_loc_pair

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )

                data.append(
                    {
                        "letter": letter,
                        "start_position": start_pos,
                        "end_position": end_pos,
                        "blue_motion_type": blue_motion_type,
                        "blue_rotation_direction": blue_rot_dir,
                        "blue_start_location": blue_start_loc,
                        "blue_end_location": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_rotation_direction": red_rot_dir,
                        "red_start_location": red_start_loc,
                        "red_end_location": red_end_loc,
                    }
                )
        return data


ABC_Generator()
