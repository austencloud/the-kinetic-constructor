import os

def rename_svg_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.svg'):
            new_filename = filename.split('.svg')[0] + '_0.svg'
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            print(f"Renamed {filename} to {new_filename}")

if __name__ == "__main__":
    folder_path = "D:\\CODE\\Apps\\Sequence_Constructor\\images\\arrows\\shift\\pro"
    rename_svg_files(folder_path)
