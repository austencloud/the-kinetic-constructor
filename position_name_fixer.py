import os
import json
from PIL import Image, PngImagePlugin
from utilities.path_helpers import get_images_and_data_path

# Mapping from old position names to new position names
position_name_mapping = {
    'alpha1': 'alpha1',
    'alpha2': 'alpha3',
    'alpha3': 'alpha5',
    'alpha4': 'alpha7',
    'beta1': 'beta1',
    'beta2': 'beta3',
    'beta3': 'beta5',
    'beta4': 'beta7',
    'gamma1': 'gamma1',
    'gamma2': 'gamma3',
    'gamma3': 'gamma5',
    'gamma4': 'gamma7',
    'gamma5': 'gamma9',
    'gamma6': 'gamma11',
    'gamma7': 'gamma13',
    'gamma8': 'gamma15',
}

def update_metadata_positions(metadata):
    # Update 'sequence_start_position' in the first item if present
    if 'sequence' in metadata and len(metadata['sequence']) > 0:
        first_item = metadata['sequence'][0]
        if 'sequence_start_position' in first_item:
            # strip off whatever numbers are after alpha, beta, or gamma
            old_pos = first_item['sequence_start_position']
            # the new pos will be the same as the old pos, but remove all numbers after the letter
            new_pos = ''.join([i for i in old_pos if not i.isdigit()])
            first_item['sequence_start_position'] = new_pos
        if "end_pos" in first_item:
            old_pos = first_item['end_pos']
            new_pos = position_name_mapping.get(old_pos, old_pos)
            first_item['end_pos'] = new_pos
            
    # Update 'start_pos' and 'end_pos' in each sequence item
    for item in metadata.get('sequence', []):
        for pos_key in ['start_pos', 'end_pos']:
            if pos_key in item:
                old_pos = item[pos_key]
                new_pos = position_name_mapping.get(old_pos, old_pos)
                item[pos_key] = new_pos
    return metadata

def update_all_metadata():
    dictionary_dir = get_images_and_data_path("dictionary")
    for root, dirs, files in os.walk(dictionary_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Add other image formats if needed
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
