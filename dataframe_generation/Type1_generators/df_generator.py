from typing import Dict, List, Tuple
import pandas as pd
from data.Enums import Location, RotationDirection, SpecificPosition
from data.constants import *
from data.positions_map import positions_map
import os


class DataFrameGenerator:
    def __init__(self, letters) -> None:
        self.letters = letters
        self.rotation_directions = ["cw", "ccw"]

    def define_shifts(
        self, shift_type
    ) -> Dict[RotationDirection, List[Tuple[Location, Location]]]:
        if shift_type == "pro":
            return {
                "cw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
                "ccw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
            }
        else:  # anti
            return {
                "cw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
                "ccw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
            }

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
        return opposite_map.get(location, "")

    def get_Type1_start_and_end_pos(
        self, red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
    ) -> Tuple[SpecificPosition, SpecificPosition]:
        start_key = (red_start_loc, RED, blue_start_loc, BLUE)
        end_key = (red_end_loc, RED, blue_end_loc, BLUE)
        start_pos = positions_map.get(start_key)
        end_pos = positions_map.get(end_key)
        return start_pos, end_pos

    def save_dataframe(self, letter, data, type_name):
        df = pd.DataFrame(data)
        self.prepare_dataframe(df)
        self.write_dataframe_to_file(
            df, f"dataframes/{type_name}/{letter}_DataFrame.csv"
        )

    def prepare_dataframe(self, df: pd.DataFrame) -> None:
        motion_type_order = ["pro", "anti", "dash", "static"]
        rotation_direction_order = ["cw", "ccw"]
        df["blue_motion_type"] = pd.Categorical(
            df["blue_motion_type"], categories=motion_type_order, ordered=True
        )
        df["blue_rotation_direction"] = pd.Categorical(
            df["blue_rotation_direction"],
            categories=rotation_direction_order,
            ordered=True,
        )
        df.sort_values(by=["letter", "blue_motion_type", "blue_rotation_direction"], inplace=True)

    def write_dataframe_to_file(self, df, filename):
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        df.to_csv(filename, index=False)

    def generate_dataframes(self) -> None:
        for letter in self.letters:
            data = getattr(self, f"create_dataframe_for_{letter}")()
            self.save_dataframe(letter, data, self.type_name)
