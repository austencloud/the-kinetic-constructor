from typing import List
from df_generator import DataFrameGenerator, BLUE, RED, positions_map


class ABC_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["A", "B", "C"])
        self.create_dataframes_for_ABC()

    def create_dataframes_for_ABC(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[dict]:
        if letter == "A":
            return self.create_dataframe_for_A()
        elif letter == "B":
            return self.create_dataframe_for_B()
        elif letter == "C":
            return self.create_dataframe_for_C()

    def create_dataframe_for_A(self) -> List[dict]:
        return self.create_dataframes_for_letter("A", "pro", "pro")

    def create_dataframe_for_B(self) -> List[dict]:
        return self.create_dataframes_for_letter("B", "anti", "anti")

    def create_dataframe_for_C(self) -> List[dict]:
        data = self.create_dataframes_for_letter("C", "pro", "anti")
        data.extend(self.create_dataframes_for_letter("C", "anti", "pro"))
        return data

    def create_dataframes_for_letter(
        self, letter, red_motion, blue_motion
    ) -> List[dict]:
        data = []
        for red_direction in self.rotation_directions:
            red_shifts = self.define_shifts(red_motion)[red_direction]
            for red_loc_pair in red_shifts:
                red_start_loc, red_end_loc = red_loc_pair
                blue_direction = self.get_opposite_direction_if_hybrid(
                    letter, red_direction
                )
                blue_loc_pair = self.get_opposite_shifts(red_loc_pair)
                blue_start_loc, blue_end_loc = blue_loc_pair

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )

                data.append(
                    self.create_data_point(
                        letter,
                        start_pos,
                        end_pos,
                        red_start_loc,
                        red_end_loc,
                        blue_start_loc,
                        blue_end_loc,
                        red_motion,
                        blue_motion,
                        red_direction,
                        blue_direction,
                    )
                )
        return data

    def get_opposite_direction_if_hybrid(self, letter, direction):
        if letter == "C":
            return "cw" if direction == "ccw" else "ccw"
        return direction

    def get_opposite_shifts(self, red_loc_pair):
        return tuple(self.get_opposite_location(loc) for loc in red_loc_pair)

    def create_data_point(
        self,
        letter,
        start_pos,
        end_pos,
        red_start_loc,
        red_end_loc,
        blue_start_loc,
        blue_end_loc,
        red_motion,
        blue_motion,
        red_direction,
        blue_direction,
    ) -> dict:
        return {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": blue_motion,
            "blue_rotation_direction": blue_direction,
            "blue_start_location": blue_start_loc,
            "blue_end_location": blue_end_loc,
            "red_motion_type": red_motion,
            "red_rotation_direction": red_direction,
            "red_start_location": red_start_loc,
            "red_end_location": red_end_loc,
        }


ABC_Generator()
