import json
import re
import pandas as pd
from typing import Dict, List, Literal

IN = "in"
OUT = "out"
CLOCKWISE = "cw"
COUNTER_CLOCKWISE = "ccw"
PRO = "pro"
ANTI = "anti"
FLOAT = "float"
DASH = "dash"
STATIC = "static"

# Load preprocessed data
with open("preprocessed.json", encoding="utf-8") as f:
    data: Dict[str, List[List[Dict]]] = json.load(f)


# Combine layer1 maps
whole_turn_orientation_map = {
    (PRO, 0, IN): IN,
    (PRO, 1, IN): OUT,
    (PRO, 2, IN): IN,
    (PRO, 3, IN): OUT,
    (PRO, 0, OUT): OUT,
    (PRO, 1, OUT): IN,
    (PRO, 2, OUT): OUT,
    (PRO, 3, OUT): IN,
    (ANTI, 0, IN): OUT,
    (ANTI, 1, IN): IN,
    (ANTI, 2, IN): OUT,
    (ANTI, 3, IN): IN,
    (ANTI, 0, OUT): IN,
    (ANTI, 1, OUT): OUT,
    (ANTI, 2, OUT): IN,
    (ANTI, 3, OUT): OUT,
    (PRO, 0, CLOCKWISE): CLOCKWISE,
    (PRO, 1, CLOCKWISE): COUNTER_CLOCKWISE,
    (PRO, 2, CLOCKWISE): CLOCKWISE,
    (PRO, 3, CLOCKWISE): COUNTER_CLOCKWISE,
    (PRO, 0, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
    (PRO, 1, COUNTER_CLOCKWISE): CLOCKWISE,
    (PRO, 2, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
    (PRO, 3, COUNTER_CLOCKWISE): CLOCKWISE,
    (ANTI, 0, CLOCKWISE): COUNTER_CLOCKWISE,
    (ANTI, 1, CLOCKWISE): CLOCKWISE,
    (ANTI, 2, CLOCKWISE): COUNTER_CLOCKWISE,
    (ANTI, 3, CLOCKWISE): CLOCKWISE,
    (ANTI, 0, COUNTER_CLOCKWISE): CLOCKWISE,
    (ANTI, 1, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
    (ANTI, 2, COUNTER_CLOCKWISE): CLOCKWISE,
    (ANTI, 3, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
}

# Combine layer2 maps

# ({HANDPATH_DIRECTION}, {START_ORIENTATION}, {END_ORIENTATION}})
clockwise_handpath_half_turns_map = {
    (PRO, 0.5, IN): COUNTER_CLOCKWISE,
    (PRO, 1.5, IN): CLOCKWISE,
    (PRO, 2.5, IN): COUNTER_CLOCKWISE,
    (PRO, 0.5, OUT): CLOCKWISE,
    (PRO, 1.5, OUT): COUNTER_CLOCKWISE,
    (PRO, 2.5, OUT): CLOCKWISE,
    (ANTI, 0.5, IN): CLOCKWISE,
    (ANTI, 1.5, IN): COUNTER_CLOCKWISE,
    (ANTI, 2.5, IN): CLOCKWISE,
    (ANTI, 0.5, OUT): COUNTER_CLOCKWISE,
    (ANTI, 1.5, OUT): CLOCKWISE,
    (ANTI, 2.5, OUT): COUNTER_CLOCKWISE,
    (PRO, 0.5, CLOCKWISE): IN,
    (PRO, 1.5, CLOCKWISE): OUT,
    (PRO, 2.5, CLOCKWISE): IN,
    (PRO, 0.5, COUNTER_CLOCKWISE): OUT,
    (PRO, 1.5, COUNTER_CLOCKWISE): IN,
    (PRO, 2.5, COUNTER_CLOCKWISE): OUT,
    (ANTI, 0.5, CLOCKWISE): OUT,
    (ANTI, 1.5, CLOCKWISE): IN,
    (ANTI, 2.5, CLOCKWISE): OUT,
    (ANTI, 0.5, COUNTER_CLOCKWISE): IN,
    (ANTI, 1.5, COUNTER_CLOCKWISE): OUT,
    (ANTI, 2.5, COUNTER_CLOCKWISE): IN,
}

counter_handpath_half_turns_map = {
    (PRO, 0.5, IN): CLOCKWISE,
    (PRO, 1.5, IN): COUNTER_CLOCKWISE,
    (PRO, 2.5, IN): CLOCKWISE,
    (PRO, 0.5, OUT): COUNTER_CLOCKWISE,
    (PRO, 1.5, OUT): CLOCKWISE,
    (PRO, 2.5, OUT): COUNTER_CLOCKWISE,
    (ANTI, 0.5, IN): COUNTER_CLOCKWISE,
    (ANTI, 1.5, IN): CLOCKWISE,
    (ANTI, 2.5, IN): COUNTER_CLOCKWISE,
    (ANTI, 0.5, OUT): CLOCKWISE,
    (ANTI, 1.5, OUT): COUNTER_CLOCKWISE,
    (ANTI, 2.5, OUT): CLOCKWISE,
    (PRO, 0.5, CLOCKWISE): OUT,
    (PRO, 1.5, CLOCKWISE): IN,
    (PRO, 2.5, CLOCKWISE): OUT,
    (PRO, 0.5, COUNTER_CLOCKWISE): IN,
    (PRO, 1.5, COUNTER_CLOCKWISE): OUT,
    (PRO, 2.5, COUNTER_CLOCKWISE): IN,
    (ANTI, 0.5, CLOCKWISE): IN,
    (ANTI, 1.5, CLOCKWISE): OUT,
    (ANTI, 2.5, CLOCKWISE): IN,
    (ANTI, 0.5, COUNTER_CLOCKWISE): OUT,
    (ANTI, 1.5, COUNTER_CLOCKWISE): IN,
    (ANTI, 2.5, COUNTER_CLOCKWISE): OUT,
}


float_map = {
    (IN, "cw_hp"): CLOCKWISE,
    (IN, "ccw_hp"): COUNTER_CLOCKWISE,
    (OUT, "cw_hp"): COUNTER_CLOCKWISE,
    (OUT, "ccw_hp"): CLOCKWISE,
    (CLOCKWISE, "cw_hp"): OUT,
    (CLOCKWISE, "ccw_hp"): IN,
    (COUNTER_CLOCKWISE, "cw_hp"): IN,
    (COUNTER_CLOCKWISE, "ccw_hp"): OUT,
}


def get_handpath_direction(start_location, end_location) -> Literal["cw_hp", "ccw_hp"]:
    clockwise_paths = [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")]
    return "cw_hp" if (start_location, end_location) in clockwise_paths else "ccw_hp"


def get_end_orientation(
    start_orientation, motion_type, turns, start_location=None, end_location=None
):
    # For float motion, determine handpath direction
    handpath_direction = get_handpath_direction(start_location, end_location)
    if motion_type == FLOAT:
        key = (start_orientation, handpath_direction)
        return float_map.get(key)

    elif turns in [0, 1, 2, 3]:
        # For pro and anti motions
        if motion_type in [PRO, ANTI]:
            key = (motion_type, turns, start_orientation)
            return whole_turn_orientation_map.get(key)

        # For static motion
        if motion_type == STATIC:
            key = (PRO, turns, start_orientation)
            return whole_turn_orientation_map.get(key)

        # For dash motion
        if motion_type == DASH:
            key = (ANTI, turns, start_orientation)
            return whole_turn_orientation_map.get(key)

    elif turns in [0.5, 1.5, 2.5]:
        if handpath_direction == "cw_hp":
            map_to_use = clockwise_handpath_half_turns_map
        else:
            map_to_use = counter_handpath_half_turns_map

        if motion_type in [PRO, ANTI]:
            key = (motion_type, turns, start_orientation)
            return map_to_use.get(key)

        if motion_type == STATIC:
            key = (PRO, turns, start_orientation)
            return map_to_use.get(key)

        elif motion_type == DASH:
            key = (ANTI, turns, start_orientation)
            return map_to_use.get(key)
    return None


# Initialize a list to store comprehensive motion data
comprehensive_motion_data = []

# Process each entry in the preprocessed data
max_turns = 3
for position_pair, letters_info in data.items():
    start_position, end_position = position_pair.split("_")
    for blue_start_orientation in ["in", "out", "cw_or", "ccw_or"]:
        for red_start_orientation in ["in", "out", "cw_or", "ccw_or"]:
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
