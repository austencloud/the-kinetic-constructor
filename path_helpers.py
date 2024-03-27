import sys
import os


def get_images_and_data_path(filename) -> str:
    """This is used for resources like data and images."""
    if hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(".")
    return os.path.join(base_dir, filename)


def get_app_data_path(filename) -> str:
    """
    For use in a Windows environment, this will return the path to the appdata directory.

    This is used for files that the user will modify, such as:
    - current_sequence json
    - settings json
    - saved words
    """
    appdata_dir = os.path.join(os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet")
    os.makedirs(appdata_dir, exist_ok=True)  # Make sure the directory exists
    return os.path.join(appdata_dir, filename)


def get_dev_path(filename) -> str:
    """
    For use in a development environment, this will return the path to the current working directory.

    This is used for files that the user will modify, such as:
    - current_sequence json
    - settings json
    - saved words
    """

    base_path = os.path.abspath(".")
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, filename)


def get_user_editable_resource_path(filename) -> str:
    if getattr(sys, "frozen", False):
        path = get_app_data_path(filename)
    else:
        path = get_dev_path(filename)
    return path


def get_dictionary_path() -> str:
    if getattr(sys, "frozen", False):
        dictionary_path = os.path.join(
            os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "dictionary"
        )
    else:
        dictionary_path = os.path.join(os.getcwd(), "dictionary")
    os.makedirs(dictionary_path, exist_ok=True)
    return dictionary_path
