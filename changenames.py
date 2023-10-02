
import os

def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if "iso" in filename:
            new_filename = filename.replace("iso", "pro")
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

# Replace 'your_folder_path_here' with the path to the folder containing the files you want to rename
folder_path = 'D:\CODE\Apps\Sequence_Constructor\images\\arrows\shift\pro'
rename_files_in_folder(folder_path)
