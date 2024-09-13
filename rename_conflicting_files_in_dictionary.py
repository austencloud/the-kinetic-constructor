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
    base_name_with_ver1 = f"{base_name}_ver1"

    # Check if base_name already has a version (e.g., _ver1)
    match = version_pattern.search(base_name)
    if match:
        # If ver1 already exists in the name, check for conflicts
        if base_name_with_ver1 + extension in existing_filenames:
            # Increment version if the same ver1 exists in the parent directory
            new_filename = increment_version(base_name, extension, existing_filenames)
            return new_filename
        else:
            return f"{base_name}{extension}"
    else:
        # If no version number exists, start with ver1 unless it already exists
        if base_name_with_ver1 + extension in existing_filenames:
            # If ver1 exists, increment the version
            new_filename = increment_version(base_name, extension, existing_filenames)
            return new_filename
        else:
            # Otherwise, assign it to ver1
            return f"{base_name_with_ver1}{extension}"


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
                # Handle potential version conflicts
                new_filename = handle_version_conflict(base_name, extension, parent_files)
                new_file_path = os.path.join(parent_dir, new_filename)
            else:
                # Move file to the parent directory (two levels up)
                new_file_path = os.path.join(parent_dir, filename)

            # If the new file path already exists, resolve conflict by incrementing version
            if os.path.exists(new_file_path):
                new_filename = increment_version(base_name, extension, parent_files)
                new_file_path = os.path.join(parent_dir, new_filename)

            # Move the file
            print(f"Moving {file_path} to {new_file_path}")
            os.rename(file_path, new_file_path)


# Execute the script to move and rename files
rename_and_move_files(root_dir)
