import os
import re
import json
from PIL import Image

from utilities.path_helpers import get_images_and_data_path

class VariationNumberFixer:
    def __init__(self):
        self.base_folder = get_images_and_data_path("dictionary")

    def get_version_number(self, name):
        """
        Extract version number from a folder or file name.
        """
        match = re.search(r'_ver(\d+)', name)
        return int(match.group(1)) if match else None

    def rename_version(self, old_path, new_path):
        """
        Rename the folder or file from old_path to new_path.
        """
        if old_path == new_path:
            return  # Skip renaming if the paths are the same
        if os.path.exists(new_path):
            raise FileExistsError(f"Cannot rename {old_path} to {new_path}: destination already exists")
        os.rename(old_path, new_path)

    def extract_metadata_from_file(self, file_path):
        """
        Extract metadata from a file.
        """
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
        except Exception as e:
            print(f"Error loading sequence from thumbnail: {e}")
        return None

    def get_start_orientation(self, metadata):
        """
        Extract the start orientation from the metadata.
        """
        if metadata and "sequence" in metadata:
            for item in metadata["sequence"]:
                if "sequence_start_position" in item:
                    start_ori = item["blue_attributes"]["start_ori"]
                    return start_ori
        return None

    def ensure_sequential_versions(self):
        """
        Ensure that all versions are sequential starting from 1.
        """
        for root, dirs, files in os.walk(self.base_folder, topdown=False):
            # Handle folders
            versioned_dirs = [d for d in dirs if '_ver' in d]
            versioned_dirs.sort(key=self.get_version_number)
            for i, old_dir_name in enumerate(versioned_dirs, start=1):
                current_version = self.get_version_number(old_dir_name)
                if current_version != i:
                    new_dir_name = re.sub(r'_ver\d+', f'_ver{i}', old_dir_name)
                    old_dir_path = os.path.join(root, old_dir_name)
                    new_dir_path = os.path.join(root, new_dir_name)
                    self.rename_version(old_dir_path, new_dir_path)
                    
                    # Rename files inside the folder to match the new folder version
                    for file_name in os.listdir(new_dir_path):
                        file_version = self.get_version_number(file_name)
                        if file_version != i:
                            new_file_name = re.sub(r'_ver\d+', f'_ver{i}', file_name)
                            old_file_path = os.path.join(new_dir_path, file_name)
                            new_file_path = os.path.join(new_dir_path, new_file_name)
                            self.rename_version(old_file_path, new_file_path)

            # Handle "none_none" folders
            for dir_name in dirs:
                if "none_none" in dir_name:
                    none_none_path = os.path.join(root, dir_name)
                    for file_name in os.listdir(none_none_path):
                        file_path = os.path.join(none_none_path, file_name)
                        metadata = self.extract_metadata_from_file(file_path)
                        start_orientation = self.get_start_orientation(metadata)
                        if start_orientation:
                            new_dir_name = dir_name.replace("none_none", start_orientation)
                            new_dir_path = os.path.join(root, new_dir_name)
                            if new_dir_path != none_none_path:  # Avoid renaming to the same path
                                self.rename_version(none_none_path, new_dir_path)
                                break  # Rename once and move on

            # Handle files in the current directory (not within a renamed sub-directory)
            versioned_files = [f for f in files if '_ver' in f]
            versioned_files.sort(key=self.get_version_number)
            for i, old_file_name in enumerate(versioned_files, start=1):
                current_version = self.get_version_number(old_file_name)
                if current_version != i:
                    new_file_name = re.sub(r'_ver\d+', f'_ver{i}', old_file_name)
                    old_file_path = os.path.join(root, old_file_name)
                    new_file_path = os.path.join(root, new_file_name)
                    if old_file_path != new_file_path:  # Avoid renaming to the same path
                        self.rename_version(old_file_path, new_file_path)

    def main(self):
        self.ensure_sequential_versions()
        print("Versioning and naming cleanup completed.")

