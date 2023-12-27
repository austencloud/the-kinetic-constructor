import json
import pandas as pd
from typing import Dict, List

# Load preprocessed data
with open("preprocessed.json", encoding="utf-8") as f:
    data: Dict[str, List[List[Dict]]] = json.load(f)

# Initialize a list to store comprehensive motion data
comprehensive_motion_data = []

# Define the additional parameters for the new "dash" motion type
rot_dirs = [None, "cw", "ccw"]

max_turns = 3
for position_pair, letters_info in data.items():
    start_position, end_position = position_pair.split("_")
    for blue_start_orientation in ["in", "out", "clock", "counter"]:
        for red_start_orientation in ["in", "out", "clock", "counter"]:
            for turns in range(max_turns + 1):
                for letter_data in letters_info:
                    letter = letter_data[0]
                    motion_pairs = letter_data[1]

                    # Handling the "W-" variations with "dash" motion
                    if letter == "W-":
                        for motion_type in ["pro", "dash"]:
                            for rot_dir in rot_dirs:
                                for start_location, end_location in [
                                    ("n", "s"),
                                    ("s", "n"),
                                    ("e", "w"),
                                    ("w", "e"),
                                ]:
                                    comprehensive_motion_data.append(
                                        {
                                            "letter": letter,
                                            "start_position": start_position,
                                            "end_position": end_position,
                                            "blue_motion_type": motion_type,
                                            "blue_rot_dir": rot_dir,
                                            "blue_start_location": start_location,
                                            "blue_end_location": end_location,
                                            "blue_start_orientation": blue_start_orientation,
                                            "red_motion_type": motion_type,
                                            "red_rot_dir": rot_dir,
                                            "red_start_location": start_location,
                                            "red_end_location": end_location,
                                            "red_start_orientation": red_start_orientation,
                                        }
                                    )
                    else:
                        # Original data processing
                        blue_motion = motion_pairs[0]
                        red_motion = motion_pairs[1]

                        comprehensive_motion_data.append(
                            {
                                "letter": letter,
                                "start_position": start_position,
                                "end_position": end_position,
                                "blue_motion_type": blue_motion["motion_type"],
                                "blue_rot_dir": blue_motion["rot_dir"],
                                "blue_start_location": blue_motion["start_location"],
                                "blue_end_location": blue_motion["end_location"],
                                "blue_start_orientation": blue_start_orientation,
                                "red_motion_type": red_motion["motion_type"],
                                "red_rot_dir": red_motion["rot_dir"],
                                "red_start_location": red_motion["start_location"],
                                "red_end_location": red_motion["end_location"],
                                "red_start_orientation": red_start_orientation,
                            }
                        )

# Convert to DataFrame, remove duplicates, sort, and save
comprehensive_df = pd.DataFrame(comprehensive_motion_data)
comprehensive_df.drop_duplicates(inplace=True)
comprehensive_df.sort_values(by=["letter", "start_position"], inplace=True)
comprehensive_df.to_csv("PictographDataframe.csv", index=False)
print("Comprehensive DataFrame with all variations created and saved.")
