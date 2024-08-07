import os
import re
import shutil
import json
from PIL import Image

def extract_metadata_from_file(file_path):
    try:
        with Image.open(file_path) as img:
            metadata = img.info.get("metadata")
            if metadata:
                return json.loads(metadata)
    except Exception as e:
        print(f"Error loading sequence from thumbnail: {e}")
    return None

def get_start_orientations(metadata):
    if metadata and "sequence" in metadata:
        start_pos_dict = metadata[1]
        if "sequence_start_position" in start_pos_dict:
            blue_ori = start_pos_dict["blue_attributes"].get("start_ori", "none")
            red_ori = start_pos_dict["red_attributes"].get("start_ori", "none")
            return f"({blue_ori},{red_ori})"
    return "(none,none)"

def reorganize_directory(base_path):
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if "ver" in dir_name:
                version_match = re.search(r'ver(\d+)', dir_name)
                if version_match:
                    version_number = version_match.group(1)
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if not os.path.exists(file_path):
                            print(f"File not found: {file_path}")
                            continue
                        metadata = extract_metadata_from_file(file_path)
                        start_orientations = get_start_orientations(metadata)
                        new_dir_name = dir_name.replace("ver", "struct")
                        new_dir_path = os.path.join(root, new_dir_name)
                        version_path = os.path.join(new_dir_path, f"ver{version_number}")
                        final_path = os.path.join(version_path, start_orientations.replace(" ", "").replace(",", "_"))
                        os.makedirs(final_path, exist_ok=True)
                        try:
                            shutil.move(file_path, os.path.join(final_path, file_name))
                        except PermissionError:
                            print(f"PermissionError: {file_path}")
                            print(f"Attempting to remove {dir_path}")
                            shutil.rmtree(dir_path)
                            print(f"Removed {dir_path}")
                            os.makedirs(final_path, exist_ok=True)
                            shutil.move(file_path, os.path.join(final_path, file_name))
                    # ensure the dir path is writable
                    if not os.access(dir_path, os.W_OK):
                        print(f"Attempting to remove {dir_path}")
                        shutil.rmtree(dir_path)
                        print(f"Removed {dir_path}")
                    shutil.rmtree(dir_path)

def main():
    dictionary_folder = 'F:\\CODE\\tka-sequence-constructor\\dictionary'  # Change to your dictionary folder path
    reorganize_directory(dictionary_folder)
    print("Directory reorganization completed.")

if __name__ == "__main__":
    main()
