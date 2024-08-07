import os


def list_directory_contents(dir_path):
    for root, dirs, files in os.walk(dir_path):
        level = root.replace(dir_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")


def main():
    directory = r"F:\CODE\tka-sequence-constructor\dictionary\EΣQY"  # Change to your directory path
    print(f"Listing contents of directory: {directory}\n")
    list_directory_contents(directory)


if __name__ == "__main__":
    main()
