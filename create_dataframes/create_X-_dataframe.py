import pandas as pd

import sys
from pathlib import Path

from constants import *  # Three dots because you're going up three levels from create_dataframes/
from data.positions_map import positions_map
from itertools import product


class Create_X_Dash_Dataframe:
    # Define basic elements
    def __init__(self) -> None:
        letters = ["X-"]
        rotation_directions = ["cw", "ccw"]
        orientations = ["in", "out", "clock", "counter"]

        # Define anti motion combinations for cw and ccw
        shifts = {
            "cw": [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")],
            "ccw": [("n", "w"), ("w", "s"), ("s", "e"), ("e", "n")],
        }
        dashes = {("n", "s"), ("e", "w"), ("s", "n"), ("w", "e")}

        # Function to get the opposite location
        def get_opposite_location(location: str) -> str:
            opposite_map = {"n": "s", "s": "n", "e": "w", "w": "e"}
            return opposite_map.get(location, "")

        # Generate combinations with left in anti and right in dash
        comprehensive_motion_data = []
        for letter, rotation_direction in product(letters, rotation_directions):
            for blue_pro_start_loc, blue_pro_end_loc in shifts[rotation_direction]:
                red_dash_start_loc = blue_pro_end_loc
                red_dash_end_loc = get_opposite_location(red_dash_start_loc)

                # Determine start and end positions for both motions
                start_pos = positions_map.get(
                    (red_dash_start_loc, RED, blue_pro_start_loc, BLUE)
                )
                end_pos = positions_map.get(
                    (red_dash_end_loc, RED, blue_pro_end_loc, BLUE)
                )

                for blue_start_orientation in orientations:
                    for red_start_orientation in orientations:
                        if start_pos and end_pos:
                            comprehensive_motion_data.append(
                                {
                                    "letter": letter,
                                    "start_position": start_pos,
                                    "end_position": end_pos,
                                    "blue_motion_type": "anti",
                                    "blue_rotation_direction": rotation_direction,
                                    "blue_start_location": blue_pro_start_loc,
                                    "blue_end_location": blue_pro_end_loc,
                                    "blue_start_orientation": blue_start_orientation,
                                    "red_motion_type": "dash",
                                    "red_rotation_direction": "None",
                                    "red_start_location": red_dash_start_loc,
                                    "red_end_location": red_dash_end_loc,
                                    "red_start_orientation": red_start_orientation,
                                }
                            )

        # Generate combinations with left in dash and right in anti
        for letter, rotation_direction in product(letters, rotation_directions):
            for red_pro_start_loc, red_pro_end_loc in shifts[rotation_direction]:
                blue_dash_start_loc = red_pro_end_loc
                blue_dash_end_loc = get_opposite_location(blue_dash_start_loc)

                # Determine start and end positions for both motions
                start_pos = positions_map.get(
                    (red_pro_start_loc, RED, blue_dash_start_loc, BLUE)
                )
                end_pos = positions_map.get(
                    (red_pro_end_loc, RED, blue_dash_end_loc, BLUE)
                )

                for blue_start_orientation in orientations:
                    for red_start_orientation in orientations:
                        if start_pos and end_pos:
                            comprehensive_motion_data.append(
                                {
                                    "letter": letter,
                                    "start_position": start_pos,
                                    "end_position": end_pos,
                                    "blue_motion_type": "dash",
                                    "blue_rotation_direction": "None",
                                    "blue_start_location": blue_dash_start_loc,
                                    "blue_end_location": blue_dash_end_loc,
                                    "blue_start_orientation": blue_start_orientation,
                                    "red_motion_type": "anti",
                                    "red_rotation_direction": rotation_direction,
                                    "red_start_location": red_pro_start_loc,
                                    "red_end_location": red_pro_end_loc,
                                    "red_start_orientation": red_start_orientation,
                                }
                            )

        # Convert to DataFrame and sort
        comprehensive_df = pd.DataFrame(comprehensive_motion_data)
        comprehensive_df.sort_values(
            by=["letter", "blue_motion_type", "start_position"], inplace=True
        )

        comprehensive_df.to_csv(
            os.path.join(os.path.dirname(__file__), "X-DataFrame.csv"), index=False
        )
        print("X- DataFrame created and saved.")


Create_X_Dash_Dataframe()
