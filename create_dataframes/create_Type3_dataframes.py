import pandas as pd
from data.constants import *
from data.positions_map import positions_map
import os


class Create_Type3_Dataframes:
    def __init__(self) -> None:
        self.letters = ["W-", "X-", "θ-", "Ω-", "Σ-", "Δ-", "Y-", "Z-"]
        self.rotation_directions = ["cw", "ccw"]
        self.pro_shifts = self.define_shifts("pro")
        self.anti_shifts = self.define_shifts("anti")
        self.generate_all_dataframes()

    def define_shifts(self, shift_type):
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

    def generate_all_dataframes(self):
        for letter in self.letters:
            self.create_dataframe_for_letter(letter)

    def create_dataframe_for_letter(self, letter):
        data = []
        for rotation_direction in self.rotation_directions:
            shift_method = (
                self.process_pro_shifts
                if letter in ["W-", "Y-", "Σ-", "θ-"]
                else self.process_anti_shifts
            )
            shift_method(letter, rotation_direction, data)
        self.save_dataframe(letter, data)

    def process_pro_shifts(self, letter, rotation_direction, data):
        for shift_start_loc, shift_end_loc in self.pro_shifts[rotation_direction]:
            dash_start_loc, dash_end_loc = self.get_dash_locations(
                letter, shift_start_loc, shift_end_loc
            )
            shift_motion_type, dash_motion_type = "pro", "dash"
            self.add_data_point(
                letter,
                shift_start_loc,
                shift_end_loc,
                dash_start_loc,
                dash_end_loc,
                rotation_direction,
                shift_motion_type,
                dash_motion_type,
                data,
            )

    def process_anti_shifts(self, letter, rotation_direction, data):
        for shift_start_loc, shift_end_loc in self.anti_shifts[rotation_direction]:
            dash_start_loc, dash_end_loc = self.get_dash_locations(
                letter, shift_start_loc, shift_end_loc
            )
            shift_motion_type, dash_motion_type = "anti", "dash"
            self.add_data_point(
                letter,
                shift_start_loc,
                shift_end_loc,
                dash_start_loc,
                dash_end_loc,
                rotation_direction,
                shift_motion_type,
                dash_motion_type,
                data,
            )

    def get_dash_locations(self, letter, shift_start_loc, shift_end_loc):
        if letter in ["W-", "X-"]:  # Dash starts at shift_end_loc
            dash_start_loc = shift_end_loc
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        elif letter in ["Y-", "Z-"]:  # Dash ends at shift_end_loc
            dash_start_loc = self.get_opposite_location(shift_end_loc)
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        elif letter in ["θ-", "Ω-"]:  # Dash ends at shift_start_loc
            dash_end_loc = shift_start_loc
            dash_start_loc = self.get_opposite_location(dash_end_loc)
        elif letter in ["Σ-", "Δ-"]:  # Dash starts at shift_start_loc
            dash_start_loc = shift_start_loc
            dash_end_loc = self.get_opposite_location(dash_start_loc)
        return dash_start_loc, dash_end_loc

    def add_data_point(
        self,
        letter,
        shift_start_loc,
        shift_end_loc,
        dash_start_loc,
        dash_end_loc,
        rotation_direction,
        shift_motion_type,
        dash_motion_type,
        data,
    ):
        start_pos, end_pos = self.get_start_and_end_pos(
            shift_start_loc, shift_end_loc, dash_start_loc, dash_end_loc
        )
        if start_pos and end_pos:
            data.append(
                self.create_data_dict(
                    letter,
                    shift_start_loc,
                    shift_end_loc,
                    dash_start_loc,
                    dash_end_loc,
                    rotation_direction,
                    shift_motion_type,
                    dash_motion_type,
                    start_pos,
                    end_pos,
                )
            )

    def get_start_and_end_pos(
        self, shift_start_loc, shift_end_loc, dash_start_loc, dash_end_loc
    ):
        start_pos = positions_map.get((dash_start_loc, RED, shift_start_loc, BLUE))
        end_pos = positions_map.get((dash_end_loc, RED, shift_end_loc, BLUE))
        return start_pos, end_pos

    def create_data_dict(
        self,
        letter,
        shift_start_loc,
        shift_end_loc,
        dash_start_loc,
        dash_end_loc,
        rotation_direction,
        shift_motion_type,
        dash_motion_type,
        start_pos,
        end_pos,
    ):
        return {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": shift_motion_type,
            "blue_rotation_direction": rotation_direction
            if shift_motion_type != "dash"
            else "None",
            "blue_start_location": shift_start_loc,
            "blue_end_location": shift_end_loc,
            "red_motion_type": dash_motion_type,
            "red_rotation_direction": rotation_direction
            if dash_motion_type != "dash"
            else "None",
            "red_start_location": dash_start_loc,
            "red_end_location": dash_end_loc,
        }

    def save_dataframe(self, letter, data):
        df = pd.DataFrame(data)
        motion_type_order = ["pro", "anti", "dash", "static"]
        df["blue_motion_type"] = pd.Categorical(
            df["blue_motion_type"], categories=motion_type_order, ordered=True
        )
        df.sort_values(
            by=["letter", "blue_motion_type", "start_position"], inplace=True
        )
        filename = f"{letter}_DataFrame.csv"
        df.to_csv(os.path.join(os.path.dirname(__file__), filename), index=False)
        print(f"{filename} created and saved.")


Create_Type3_Dataframes()
