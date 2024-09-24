import os
import json
from PIL import Image, PngImagePlugin
from utilities.path_helpers import get_images_and_data_path

# New positions_map using string values directly
positions_map = {
    ('s', 'n'): 'alpha1',
    ('sw', 'ne'): 'alpha2',
    ('w', 'e'): 'alpha3',
    ('nw', 'se'): 'alpha4',
    ('n', 's'): 'alpha5',
    ('ne', 'sw'): 'alpha6',
    ('e', 'w'): 'alpha7',
    ('se', 'nw'): 'alpha8',
    ('n', 'n'): 'beta1',
    ('ne', 'ne'): 'beta2',
    ('e', 'e'): 'beta3',
    ('se', 'se'): 'beta4',
    ('s', 's'): 'beta5',
    ('sw', 'sw'): 'beta6',
    ('w', 'w'): 'beta7',
    ('nw', 'nw'): 'beta8',
    ('w', 'n'): 'gamma1',
    ('nw', 'ne'): 'gamma2',
    ('n', 'e'): 'gamma3',
    ('ne', 'se'): 'gamma4',
    ('e', 's'): 'gamma5',
    ('se', 'sw'): 'gamma6',
    ('s', 'w'): 'gamma7',
    ('sw', 'nw'): 'gamma8',
    ('e', 'n'): 'gamma9',
    ('se', 'ne'): 'gamma10',
    ('s', 'e'): 'gamma11',
    ('sw', 'se'): 'gamma12',
    ('w', 's'): 'gamma13',
    ('nw', 'sw'): 'gamma14',
    ('n', 'w'): 'gamma15',
    ('ne', 'nw'): 'gamma16',
}

def compute_positions(blue_attributes, red_attributes):
    blue_start_loc = blue_attributes.get('start_loc')
    red_start_loc = red_attributes.get('start_loc')
    blue_end_loc = blue_attributes.get('end_loc')
    red_end_loc = red_attributes.get('end_loc')

    # Handle missing or invalid locations
    if None in (blue_start_loc, red_start_loc, blue_end_loc, red_end_loc):
        print(f"Invalid location in attributes: {blue_attributes}, {red_attributes}")
        return "unknown", "unknown"

    # For start_pos, use (blue_start_loc, red_start_loc)
    start_pos_tuple = (blue_start_loc, red_start_loc)
    # For end_pos, use (red_end_loc, blue_end_loc)
    end_pos_tuple = (red_end_loc, blue_end_loc)

    # Get positions from positions_map
    start_pos = positions_map.get(start_pos_tuple, "unknown")
    end_pos = positions_map.get(end_pos_tuple, "unknown")

    if start_pos == "unknown":
        print(f"Warning: start position not found for {start_pos_tuple}")
    if end_pos == "unknown":
        print(f"Warning: end position not found for {end_pos_tuple}")

    return start_pos, end_pos

def update_metadata_positions(metadata):
    sequence = metadata.get("sequence", [])
    if not sequence:
        return metadata

    # For the initial beat (sequence[1]), compute sequence_start_position
    if len(sequence) > 1:
        initial_beat = sequence[1]
        blue_attributes = initial_beat["blue_attributes"]
        red_attributes = initial_beat["red_attributes"]

        # Compute sequence_start_position
        blue_start_loc = blue_attributes.get('start_loc')
        red_start_loc = red_attributes.get('start_loc')
        start_pos_tuple = (blue_start_loc, red_start_loc)
        sequence_start_position = positions_map.get(start_pos_tuple, "unknown")

        if sequence_start_position == "unknown":
            print(f"Warning: sequence_start_position not found for {start_pos_tuple}")

        # Update sequence_start_position in the initial beat
        initial_beat["sequence_start_position"] = sequence_start_position

    # For each beat, compute start_pos and end_pos
    for item in sequence[1:]:
        blue_attributes = item.get("blue_attributes", {})
        red_attributes = item.get("red_attributes", {})

        start_pos, end_pos = compute_positions(blue_attributes, red_attributes)

        item["start_pos"] = start_pos
        item["end_pos"] = end_pos

    return metadata

def update_all_metadata():
    dictionary_dir = get_images_and_data_path("dictionary")
    for root, dirs, files in os.walk(dictionary_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                print(f'Processing file: {file_path}')
                try:
                    with Image.open(file_path) as img:
                        metadata = img.info.get('metadata')
                        if metadata:
                            metadata_dict = json.loads(metadata)
                            updated_metadata = update_metadata_positions(metadata_dict)
                            # Save the image with updated metadata
                            pnginfo = PngImagePlugin.PngInfo()
                            pnginfo.add_text('metadata', json.dumps(updated_metadata))
                            img.save(file_path, pnginfo=pnginfo)
                            print(f'Updated metadata for {file_path}')
                        else:
                            print(f'No metadata found in {file_path}')
                except Exception as e:
                    print(f'Error processing {file_path}: {e}')

if __name__ == '__main__':
    update_all_metadata()
