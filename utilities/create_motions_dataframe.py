import json
import pandas as pd
from typing import Dict, List


# Load preprocessed data
with open("preprocessed.json", encoding="utf-8") as f:
    data: Dict[str, List[List[Dict]]] = json.load(f)

# Initialize a list to store comprehensive motion data
comprehensive_motion_data = []

# Process each entry in the preprocessed data
max_turns = 3
for position_pair, letters_info in data.items():
    start_position, end_position = position_pair.split("_")
    for blue_start_orientation in ["in", "out", "clock", "counter"]:
        for red_start_orientation in ["in", "out", "clock", "counter"]:
            for turns in range(max_turns + 1):
                for letter_data in letters_info:
                    letter = letter_data[0]
                    motion_pairs = letter_data[1]

                    blue_motion = motion_pairs[0]
                    red_motion = motion_pairs[1]

                    motion_data_entry = {
                        "letter": letter,
                        "start_position": start_position,
                        "end_position": end_position,
                        "blue_motion_type": blue_motion["motion_type"],
                        "blue_rotation_direction": blue_motion["rotation_direction"],
                        "blue_start_location": blue_motion["start_location"],
                        "blue_end_location": blue_motion["end_location"],
                        "blue_start_orientation": blue_start_orientation,
                        "red_motion_type": red_motion["motion_type"],
                        "red_rotation_direction": red_motion["rotation_direction"],
                        "red_start_location": red_motion["start_location"],
                        "red_end_location": red_motion["end_location"],
                        "red_start_orientation": red_start_orientation,
                    }

                    comprehensive_motion_data.append(motion_data_entry)

# Convert to DataFrame, remove duplicates, sort, and save
comprehensive_df = pd.DataFrame(comprehensive_motion_data)
comprehensive_df.drop_duplicates(inplace=True)
comprehensive_df.sort_values(by=["letter", "start_position"], inplace=True)
comprehensive_df.to_csv("PictographDataframe.csv", index=False)
print("Comprehensive DataFrame with all variations created and saved.")
