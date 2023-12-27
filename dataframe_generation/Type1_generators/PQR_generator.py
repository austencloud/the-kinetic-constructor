from df_generator import DataFrameGenerator
from typing import Dict, List


class PQR_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["P", "Q", "R"])
        self.create_dataframes_for_PQR()

    def create_dataframes_for_PQR(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter == "P":
            return self.create_dataframes_for_letter("P", "pro", "pro")
        elif letter == "Q":
            return self.create_dataframes_for_letter("Q", "anti", "anti")
        elif letter == "R":
            data = self.create_dataframes_for_letter("R", "pro", "anti")
            data += self.create_dataframes_for_letter("R", "anti", "pro")
            return data

    def create_dataframe_for_D(self) -> List[Dict]:
        return self.create_dataframes_for_letter("P", "pro", "pro")

    def create_dataframe_for_E(self) -> List[Dict]:
        return self.create_dataframes_for_letter("Q", "anti", "anti")

    def create_dataframe_for_F(self) -> List[Dict]:
        data = self.create_dataframes_for_letter("R", "pro", "anti")
        data.extend(self.create_dataframes_for_letter("R", "anti", "pro"))
        return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        for red_rot_dir in self.rot_dirs:
            red_shifts = self.define_rot_dir_mapping(red_motion_type)[red_rot_dir]
            for red_loc_pair in red_shifts:
                red_start_loc, red_end_loc = red_loc_pair
                if self.is_hybrid(letter):
                    blue_rot_dir = red_rot_dir
                else:
                    blue_rot_dir = self.get_opposite_rot_dir(red_rot_dir)
                blue_loc_pair = (red_end_loc, red_start_loc)
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
                        "blue_rot_dir": blue_rot_dir,
                        "blue_start_location": blue_start_loc,
                        "blue_end_location": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_rot_dir": red_rot_dir,
                        "red_start_location": red_start_loc,
                        "red_end_location": red_end_loc,
                    }
                )
        return data

    # The rest of the methods from DataFrameGenerator remain unchanged.


PQR_Generator()
