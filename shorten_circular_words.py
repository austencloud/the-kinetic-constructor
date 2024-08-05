import os
import re
import shutil

def shorten_word(word):
    """Shorten repeated words in a given string if applicable."""
    match = re.match(r"^(.*?)\1+$", word)
    return match.group(1) if match else word

def extract_and_shorten_base(word):
    """Extract base word, shorten it, and reattach the suffix."""
    # Split the word into base and suffix
    base_word, _, suffix = word.partition('_ver')
    shortened_base = shorten_word(base_word)
    return shortened_base + (f'_ver{suffix}' if suffix else '')

def process_path(path):
    """Process the folder and file names to shorten repeated words."""
    parts = path.split(os.sep)
    shortened_parts = []
    for part in parts:
        if '_ver' in part:
            shortened_parts.append(extract_and_shorten_base(part))
        else:
            shortened_parts.append(shorten_word(part))
    return os.sep.join(shortened_parts)

def increment_version(path):
    """Increment the version number of a path if it exists."""
    base, ext = os.path.splitext(path)
    match = re.search(r"(_ver)(\d+)$", base)
    if match:
        base, ver_num = base[:match.start()], int(match.group(2))
        new_path = f"{base}_ver{ver_num + 1}{ext}"
    else:
        new_path = f"{base}_ver1{ext}"
    if os.path.exists(new_path):
        return increment_version(new_path)
    return new_path

def rename_folder_and_files(base_path):
    for dirpath, dirnames, filenames in os.walk(base_path, topdown=False):
        print(f"Processing directory: {dirpath}")  # Debug statement

        # Process files
        for filename in filenames:
            old_filepath = os.path.join(dirpath, filename)
            new_filename = process_path(filename)
            new_filepath = os.path.join(dirpath, new_filename)
            if old_filepath != new_filepath:
                if os.path.exists(new_filepath):
                    new_filepath = increment_version(new_filepath)
                print(f"Renaming file: {old_filepath} -> {new_filepath}")  # Debug statement
                os.rename(old_filepath, new_filepath)

        # Process folders
        for dirname in dirnames:
            old_dirpath = os.path.join(dirpath, dirname)
            new_dirname = process_path(dirname)
            new_dirpath = os.path.join(dirpath, new_dirname)

            if old_dirpath != new_dirpath:
                if not os.path.exists(new_dirpath):
                    os.rename(old_dirpath, new_dirpath)
                else:
                    print(f"Conflict detected: {new_dirpath} already exists")  # Debug statement
                    # Increment the version number for the new directory path
                    new_dirpath = increment_version(new_dirpath)
                    print(f"Renaming folder: {old_dirpath} -> {new_dirpath}")  # Debug statement
                    os.rename(old_dirpath, new_dirpath)

def main():
    dictionary_path = r"F:\CODE\tka-sequence-constructor\dictionary"
    print(f"Starting renaming process in {dictionary_path}")  # Debug statement
    rename_folder_and_files(dictionary_path)
    print("Renaming process completed.")  # Debug statement

if __name__ == "__main__":
    main()
