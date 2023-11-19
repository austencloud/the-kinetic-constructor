import os
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

def resize_svg(file_path, output_size=(120, 120)) -> ElementTree:
    # Parse the original SVG file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the width and height of the original SVG
    original_width = int(root.get("width", "0").replace("px", ""))
    original_height = int(root.get("height", "0").replace("px", ""))

    # Calculate the new dimensions and offsets
    new_width, new_height = output_size
    x_offset = (new_width - original_width) / 2
    y_offset = (new_height - original_height) / 2

    # Update the viewBox and size attributes
    root.set("width", str(new_width))
    root.set("height", str(new_height))
    root.set("viewBox", f"0 0 {new_width} {new_height}")

    # Adjust the position of each element
    for element in root.findall(".//*"):
        if 'transform' in element.attrib:
            current_transform = element.get('transform')
            element.set('transform', f'translate({x_offset}, {y_offset}) {current_transform}')
        else:
            element.set('transform', f'translate({x_offset}, {y_offset})')

    return tree

def process_svgs(directory) -> None:
    for subdir, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".svg"):
                file_path = os.path.join(subdir, filename)
                resized_svg = resize_svg(file_path)
                resized_svg.write(file_path)  # Overwrites the original file

# Directory containing SVG files (modify as needed)
directory = "resources/images/letters"

process_svgs(directory)
