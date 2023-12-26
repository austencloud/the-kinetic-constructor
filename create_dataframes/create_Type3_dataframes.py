
import pandas as pd
from data.constants import *
from data.positions_map import positions_map
import os

class Create_Type3_Dataframes:
    def __init__(self) -> None:
        self.letters = ["W-", "X-", "θ-", "Ω-"]
        self.rotation_directions = ["cw", "ccw"]
        self.pro_shifts = {
            "cw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
            "ccw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
        }
        self.anti_shifts = {
            "cw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
            "ccw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
        }
        self.create_all_dataframes()

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
        return opposite_map.get(location, "")

    def create_all_dataframes(self):
        for letter in self.letters:
            self.create_dash_dataframe(letter)

    def create_dash_dataframe(self, letter) -> None:
        data = []
        for rotation_direction in self.rotation_directions:
            if letter in ["W-", "θ-"]:
                self.process_pro_shifts(letter, rotation_direction, data)
            elif letter in ["X-", "Ω-"]:
                self.process_anti_shifts(letter, rotation_direction, data)
        self.save_dataframe(letter, data)

    def process_pro_shifts(self, letter, rotation_direction, data):
        for start_loc, end_loc in self.pro_shifts[rotation_direction]:
            if letter == "W-":
                self.add_data_point(letter, start_loc, end_loc, rotation_direction, "pro", "dash", data)
                self.add_data_point(letter, end_loc, start_loc, "None", "dash", "pro", data)
            elif letter == "θ-":
                self.add_data_point(letter, end_loc, start_loc, "None", "dash", "pro", data, end_loc)
                self.add_data_point(letter, start_loc, end_loc, rotation_direction, "pro", "dash", data, start_loc)

    def process_anti_shifts(self, letter, rotation_direction, data):
        for start_loc, end_loc in self.anti_shifts[rotation_direction]:
            if letter == "X-":
                self.add_data_point(letter, start_loc, end_loc, rotation_direction, "anti", "dash", data)
                self.add_data_point(letter, end_loc, start_loc, "None", "dash", "anti", data)
            elif letter == "Ω-":
                self.add_data_point(letter, end_loc, start_loc, "None", "dash", "anti", data, end_loc)
                self.add_data_point(letter, start_loc, end_loc, rotation_direction, "anti", "dash", data, start_loc)

    def add_data_point(self, letter, start_loc, end_loc, rotation_direction, blue_motion_type, red_motion_type, data, dash_end_loc=None):
        red_end_loc = self.get_opposite_location(end_loc) if not dash_end_loc else dash_end_loc
        red_start_loc = self.get_opposite_location(start_loc) if dash_end_loc else end_loc

        start_pos, end_pos = self.get_start_and_end_pos(start_loc, end_loc, red_start_loc, red_end_loc)

        if start_pos and end_pos:
            data.append(
                self.create_data_dict(
                    letter, start_loc, end_loc, red_start_loc, red_end_loc,
                    blue_motion_type, red_motion_type, rotation_direction,
                    start_pos, end_pos
                )
            )

    def get_start_and_end_pos(self, start_loc, end_loc, red_start_loc, red_end_loc):
        start_pos = positions_map.get((red_start_loc, RED, start_loc, BLUE))
        end_pos = positions_map.get((red_end_loc, RED, end_loc, BLUE))
        return start_pos, end_pos

    def create_data_dict(self, letter, start_loc, end_loc, red_start_loc, red_end_loc, blue_motion_type, red_motion_type, rotation_direction, start_pos, end_pos):
        return {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": blue_motion_type,
            "blue_rotation_direction": rotation_direction,
            "blue_start_location": start_loc,
            "blue_end_location": end_loc,
            "red_motion_type": red_motion_type,
            "red_rotation_direction": "None",
            "red_start_location": red_start_loc,
            "red_end_location": red_end_loc,
        }


    def save_dataframe(self, letter, data) -> None:
        df = pd.DataFrame(data)
        motion_type_order = ["pro", "anti", "dash", "static"]
        df["blue_motion_type"] = pd.Categorical(
            df["blue_motion_type"],
            categories=motion_type_order,
            ordered=True,
        )
        df.sort_values(
            by=["letter", "blue_motion_type", "start_position"], inplace=True
        )
        filename = f"{letter.replace('-', '')}-DataFrame.csv"
        df.to_csv(os.path.join(os.path.dirname(__file__), filename), index=False)
        print(f"{filename} created and saved.")



Create_Type3_Dataframes()