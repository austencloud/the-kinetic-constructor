import os
import shutil

# Root directory containing all the images
root_dir = r"F:\CODE\tka-sequence-constructor\dictionary"

def move_images_to_parent_directory(directory):
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(directory):
        for subdir in dirnames:
            subdir_path = os.path.join(dirpath, subdir)

            # List all files in the subdir
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)

                # Generate the new file path in the parent directory
                new_file_path = os.path.join(dirpath, filename)

                # Check if a file with the same name already exists in the parent directory
                if os.path.exists(new_file_path):
                    print(f"File already exists: {new_file_path}. Skipping...")
                    continue

                # Move the file from the subdirectory to the parent directory
                shutil.move(file_path, new_file_path)
                print(f"Moved: {file_path} -> {new_file_path}")

            # After all files are moved, remove the now-empty subdirectory
            try:
                if not os.listdir(subdir_path):
                    os.rmdir(subdir_path)
                    print(f"Removed empty folder: {subdir_path}")
            except PermissionError as e:
                print(f"PermissionError: {e}. Could not remove folder: {subdir_path}")
            except OSError as e:
                print(f"OSError: {e}. Could not remove folder: {subdir_path}")

if __name__ == "__main__":
    move_images_to_parent_directory(root_dir)
