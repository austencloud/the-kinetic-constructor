import os
import re

# Root directory containing all the images
root_dir = r"F:\CODE\tka-sequence-constructor\dictionary"

# Regular expression to identify the version in the file name (e.g., "_ver1", "_ver2")
version_pattern = re.compile(r"_ver(\d+)")


def increment_version(base_name, extension, existing_filenames):
    """Increments the version number to resolve file name conflicts."""
    match = version_pattern.search(base_name)
    if match:
        # Extract the current version number
        version_number = int(match.group(1))
        # Increment the version number until we find an unused version in the parent directory
        while True:
            version_number += 1
            new_base_name = version_pattern.sub(f"_ver{version_number}", base_name)
            new_filename = f"{new_base_name}{extension}"
            if new_filename not in existing_filenames:
                return new_filename
    else:
        # If there's no version number, start with _ver2
        new_base_name = f"{base_name}_ver2"
        new_filename = f"{new_base_name}{extension}"
        return new_filename


def handle_version_conflict(base_name, extension, existing_filenames):
    """Check if both files are version 1 and resolve conflicts."""
    version_1_files = [f for f in existing_filenames if "_ver1" in f]

    # If there's a conflict (multiple version 1 files), increment one of them
    if len(version_1_files) > 1:
        # Increment the version number for the current file
        new_filename = increment_version(base_name, extension, existing_filenames)
        return new_filename
    else:
        # No conflict, return the base name with version 1
        return f"{base_name}_ver1{extension}"


def get_all_files_in_directory(directory):
    """Recursively get all files in the given directory and subdirectories."""
    all_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Make sure to get the full path
            file_path = os.path.join(dirpath, filename)
            all_files.append(file_path)
    return all_files


def rename_and_move_files(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Get the full file path
            file_path = os.path.join(dirpath, filename)

            # Extract the base name and extension
            base_name, extension = os.path.splitext(filename)

            # Get the parent directory (two levels up from the current file)
            parent_dir = os.path.dirname(os.path.dirname(dirpath))

            # Get all files in the parent directory and its subdirectories
            parent_files = [
                os.path.basename(f)  # Get the filename from the full path
                for f in get_all_files_in_directory(parent_dir)
                if f.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"))
            ]

            # Ensure we compare the full filename (including extensions) in the parent directory
            if filename in parent_files:
                # Check for version conflicts and handle them
                if "_ver1" in filename:
                    # Handle potential version 1 conflicts
                    new_filename = handle_version_conflict(base_name, extension, parent_files)
                else:
                    # Increment the version number to resolve conflict in the parent directory
                    new_filename = increment_version(base_name, extension, parent_files)
                
                new_file_path = os.path.join(parent_dir, new_filename)
            else:
                # Move file to the parent directory (two levels up)
                new_file_path = os.path.join(parent_dir, filename)

            # Move the file
            print(f"Moving {file_path} to {new_file_path}")
            os.rename(file_path, new_file_path)


# Execute the script to move and rename files
rename_and_move_files(root_dir)
