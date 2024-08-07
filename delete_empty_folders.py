import os
import shutil


def is_folder_empty(folder_path):
    """
    Check if a folder is empty
    :param folder_path: Path to the folder
    :return: True if the folder is empty, False otherwise
    """
    return not any(os.scandir(folder_path))


def delete_empty_folders(root_folder):
    """
    Traverse the root folder and delete empty folders
    :param root_folder: Path to the root folder
    """
    for root, dirs, files in os.walk(root_folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if is_folder_empty(dir_path):
                #set it to writable
                os.chmod(dir_path, 0o777)
                print(f"Deleting empty folder: {dir_path}")
                shutil.rmtree(dir_path)


def main():
    dictionary_folder = "F:\\CODE\\tka-sequence-constructor\\dictionary"  # Change to your dictionary folder path
    delete_empty_folders(dictionary_folder)
    print("Cleanup completed.")


if __name__ == "__main__":
    main()
