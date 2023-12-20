import json
import os
import pandas as pd
from typing import Dict, List, Literal

from TypeChecking.Letters import Letters

# Load preprocessed data
with open("preprocessed.json", encoding="utf-8") as f:
    data: Dict[str, List[List[Dict[Letters, Dict]]]] = json.load(f)

# Initialize a list to store comprehensive motion data
comprehensive_motion_data = []


def get_end_orientation(start_orientation, motion_type, turns) -> Literal["out", "in"]:
    if motion_type in ["pro", "static"] and turns == 0:
        return start_orientation
    else:
        return "out" if start_orientation == "in" else "in"



# Process each entry in the preprocessed data
for position_pair, letters_info in data.items():
    start_position, end_position = position_pair.split(
        "_"
    )  # Extract start and end positions from the key
    for blue_start_orientation in [
        "in",
        "out",
    ]:  # Iterate over both start orientations for blue
        for red_start_orientation in [
            "in",
            "out",
        ]:  # Iterate over both start orientations for red
            for letter_data in letters_info:
                letter = letter_data[
                    0
                ]  # The letter representing the motion combination
                motion_pairs = letter_data[
                    1
                ]  # The list containing the motion pairs and optimal locations

                # Check if the motion pair has the expected structure
                if len(motion_pairs) >= 2 and all(
                    isinstance(item, dict) for item in motion_pairs[:2]
                ):
                    blue_motion = motion_pairs[0]
                    red_motion = motion_pairs[1]
                    optimal_locations = (
                        motion_pairs[2] if len(motion_pairs) == 3 else {}
                    )

                    # Calculate end orientations based on start orientation, motion type, and turns
                    blue_end_orientation = get_end_orientation(
                        blue_start_orientation,
                        blue_motion["motion_type"],
                        blue_motion["turns"],
                    )
                    red_end_orientation = get_end_orientation(
                        red_start_orientation,
                        red_motion["motion_type"],
                        red_motion["turns"],
                    )

                    # Create a dictionary entry for this motion combination
                    motion_data_entry = {
                        "letter": letter,
                        "start_position": start_position,
                        "end_position": end_position,
                        "blue_color": blue_motion["color"],
                        "blue_motion_type": blue_motion["motion_type"],
                        "blue_rotation_direction": blue_motion["rotation_direction"],
                        "blue_turns": blue_motion["turns"],
                        "blue_start_location": blue_motion["start_location"],
                        "blue_end_location": blue_motion["end_location"],
                        "blue_start_orientation": blue_start_orientation,
                        "blue_end_orientation": blue_end_orientation,
                        "blue_start_layer": 1,
                        "blue_end_layer": 1,
                        "red_color": red_motion["color"],
                        "red_motion_type": red_motion["motion_type"],
                        "red_turns": red_motion["turns"],
                        "red_rotation_direction": red_motion["rotation_direction"],
                        "red_start_location": red_motion["start_location"],
                        "red_end_location": red_motion["end_location"],
                        "red_start_orientation": red_start_orientation,
                        "red_end_orientation": red_end_orientation,
                        "red_start_layer": 1,
                        "red_end_layer": 1,
                        "optimal_blue_location": optimal_locations.get(
                            "optimal_blue_location", None
                        ),
                        "optimal_red_location": optimal_locations.get(
                            "optimal_red_location", None
                        ),
                    }


                    # Append this entry to the comprehensive data list
                    comprehensive_motion_data.append(motion_data_entry)


# Convert the list to a DataFrame
comprehensive_df = pd.DataFrame(comprehensive_motion_data)

# Sort the DataFrame by letter and start_position
comprehensive_df.sort_values(by=["letter", "start_position"], inplace=True)

# Save the DataFrame to a CSV file
comprehensive_df.to_csv("LetterDictionary.csv", index=False)
print("DataFrame created and saved.")
