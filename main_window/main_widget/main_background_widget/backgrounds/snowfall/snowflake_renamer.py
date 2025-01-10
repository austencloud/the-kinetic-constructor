import os


def rename_snowflakes(folder_path):
    # Get all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Sort files to ensure they are renamed in a predictable order
    files.sort()

    # Rename files sequentially to snowflake1.png, snowflake2.png, etc.
    for i, file_name in enumerate(files, start=1):
        # Get the file extension (e.g., .png)
        _, file_extension = os.path.splitext(file_name)

        # Create the new file name
        new_name = f"snowflake{i}{file_extension}"

        # Rename the file
        os.rename(
            os.path.join(folder_path, file_name), os.path.join(folder_path, new_name)
        )
        print(f"Renamed {file_name} to {new_name}")


# Define the folder path
folder_path = "images/snowflakes"

# Run the renaming function
rename_snowflakes(folder_path)
