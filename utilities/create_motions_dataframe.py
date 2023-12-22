import json
import pandas as pd
from typing import Dict, List, Literal

# Load preprocessed data
with open("preprocessed.json", encoding="utf-8") as f:
    data: Dict[str, List[List[Dict]]] = json.load(f)


# Function to determine end orientation
def get_end_orientation(
    start_orientation: str, motion_type: str, turns: int
) -> Literal["out", "in"]:
    if turns % 2 == 0:
        return (
            start_orientation
            if motion_type in ["pro", "static"]
            else ("out" if start_orientation == "in" else "in")
        )
    else:
        return (
            ("out" if start_orientation == "in" else "in")
            if motion_type in ["pro", "static"]
            else start_orientation
        )


# Initialize a list to store comprehensive motion data
comprehensive_motion_data = []

# Process each entry in the preprocessed data
max_turns = 3  # Define the maximum number of turns
for position_pair, letters_info in data.items():
    start_position, end_position = position_pair.split("_")
    for blue_start_orientation in ["in", "out"]:
        for red_start_orientation in ["in", "out"]:
            for turns in range(max_turns + 1):
                for blue_turns in range(turns + 1):
                    for red_turns in range(turns + 1):
                        for letter_data in letters_info:
                            letter = letter_data[0]
                            motion_pairs = letter_data[1]

                            blue_motion = motion_pairs[0]
                            red_motion = motion_pairs[1]

                            # Calculate end orientations based on start orientation, motion type, and turns
                            blue_end_orientation = get_end_orientation(
                                blue_start_orientation,
                                blue_motion["motion_type"],
                                blue_turns,
                            )
                            red_end_orientation = get_end_orientation(
                                red_start_orientation,
                                red_motion["motion_type"],
                                red_turns,
                            )


                            motion_data_entry = {
                                "letter": letter,
                                "start_position": start_position,
                                "end_position": end_position,
                                "blue_motion_type": blue_motion["motion_type"],
                                "blue_rotation_direction": blue_motion[
                                    "rotation_direction"
                                ],
                                "blue_turns": blue_turns,
                                "blue_start_location": blue_motion["start_location"],
                                "blue_end_location": blue_motion["end_location"],
                                "blue_start_orientation": blue_start_orientation,
                                "blue_end_orientation": blue_end_orientation,
                                "red_motion_type": red_motion["motion_type"],
                                "red_rotation_direction": red_motion[
                                    "rotation_direction"
                                ],
                                "red_turns": red_turns,
                                "red_start_location": red_motion["start_location"],
                                "red_end_location": red_motion["end_location"],
                                "red_start_orientation": red_start_orientation,
                                "red_end_orientation": red_end_orientation,
                            }

                            comprehensive_motion_data.append(motion_data_entry)

# Convert the list to a DataFrame and save
comprehensive_df = pd.DataFrame(comprehensive_motion_data)
comprehensive_df.sort_values(by=["letter", "start_position"], inplace=True)
comprehensive_df.to_csv("ComprehensiveMotionDictionary.csv", index=False)
print("Comprehensive DataFrame with all variations created and saved.")
