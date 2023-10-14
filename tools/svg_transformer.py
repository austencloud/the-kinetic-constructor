import os
from xml.etree import ElementTree as ET

def make_square(root, width, height):
    """Adjust the SVG to make it square by adding padding to the shorter dimension."""
    max_dim = max(width, height)
    x_offset = (max_dim - width) / 2
    y_offset = (max_dim - height) / 2
    root.attrib['viewBox'] = f"{-x_offset} {-y_offset} {max_dim} {max_dim}"
    return root, max_dim, max_dim

def resize_to_comfortable_dimension(root, width, height):
    """Resize the SVG to the nearest comfortable dimension (multiple of 10) while centering its contents."""
    comfortable_dim = round(width / 10) * 10
    scale_factor = comfortable_dim / width
    viewbox_values = [float(val) for val in root.attrib['viewBox'].split()]
    viewbox_values[2] *= scale_factor
    viewbox_values[3] *= scale_factor
    root.attrib['viewBox'] = ' '.join(map(str, viewbox_values))
    return root, comfortable_dim, comfortable_dim

def process_svg(svg_path, output_path):
    """Load the SVG, make it square, resize to comfortable dimension, and save the transformed SVG."""
    tree = ET.parse(svg_path)
    root = tree.getroot()
    viewbox_values = [float(val) for val in root.attrib['viewBox'].split()]
    width = viewbox_values[2]
    height = viewbox_values[3]
    square_root, _, _ = make_square(root, width, height)
    resized_root, _, _ = resize_to_comfortable_dimension(square_root, width, height)
    tree = ET.ElementTree(resized_root)
    tree.write(output_path)

def main():
    print("Enter the directories containing SVG files to process. Enter 'DONE' when finished.")
    directories = []
    
    while True:
        directory = input("Directory path: ")
        if directory.lower() == "done":
            break
        directories.append(directory)

    for directory_path in directories:
        svg_files = [file for file in os.listdir(directory_path) if file.endswith('.svg')]
        
        for svg_file in svg_files:
            input_path = os.path.join(directory_path, svg_file)
            output_path = os.path.join(directory_path, f"{svg_file}")
            process_svg(input_path, output_path)
            print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    main()