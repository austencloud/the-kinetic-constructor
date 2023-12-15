import json
import os

# Directory path containing the JSON files
json_dir_path = "F:/CODE/tka-app/tka-sequence-constructor/resources/json/Type 2"


# Function to process each JSON file
def process_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Iterate over each letter key (like 'W') and its list of motion sets
        for letter, motionss in data.items():
            for motions in motionss:
                # Each motions is a list, iterate over its items
                for motion in motions:
                    # Skip non-dictionary items and entries without 'motion_type'
                    if not isinstance(motion, dict) or "motion_type" not in motion:
                        continue

                    # Check if arrow_location is missing or null for static motion types
                    if motion["motion_type"] == "static" and (
                        motion.get("arrow_location") is None
                        or motion["arrow_location"] == "None"
                    ):
                        # Set arrow_location to start/end location
                        motion["arrow_location"] = motion["start_location"]

    # Overwrite the file with updated data
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Process each JSON file in the directory
for filename in os.listdir(json_dir_path):
    if filename.endswith(".json"):
        process_json_file(os.path.join(json_dir_path, filename))
