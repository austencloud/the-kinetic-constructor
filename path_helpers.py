import sys
import os


def resource_path(filename):
    """Get the absolute path to the resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


def app_data_path(filename):
    """Constructs a path to the filename in the user's AppData directory."""
    appdata_dir = os.path.join(os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet")
    os.makedirs(appdata_dir, exist_ok=True)  # Make sure the directory exists
    return os.path.join(appdata_dir, filename)


def dev_path(filename):
    """Constructs a path to the filename in the project's root directory."""
    base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)
