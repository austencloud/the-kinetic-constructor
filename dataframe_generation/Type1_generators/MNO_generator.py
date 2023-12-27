from df_generator import DataFrameGenerator


from typing import Dict, List, Tuple
from data.Enums import Location, PropRotDir
from df_generator import DataFrameGenerator


class MNO_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["M", "N", "O"])
        self.create_dataframes_for_MNO()

    def create_dataframes_for_MNO(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter == "M":
            return self.create_dataframes_for_letter("M", "pro", "pro")
        elif letter == "N":
            return self.create_dataframes_for_letter("N", "anti", "anti")
        elif letter == "O":
            # For "F", generate "pro"-"anti" and "anti"-"pro" combinations without causing recursion
            data = self.create_dataframes_for_letter("O", "pro", "anti")
            data += self.create_dataframes_for_letter("O", "anti", "pro")
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
                blue_loc_pair = self.get_opposite_loc_tuple(red_loc_pair)
                blue_loc_pair = (blue_loc_pair[1], blue_loc_pair[0])
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


MNO_Generator()
