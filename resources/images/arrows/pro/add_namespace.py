import os
import xml.etree.ElementTree as ET


def format_d_attribute(path_element, line_length=80):
    d_attr = path_element.get("d")
    if not d_attr:
        return

    # Split the 'd' attribute into lines of specified length
    formatted_d = ""
    line = ""
    for part in d_attr.split():
        if len(line) + len(part) < line_length:
            line += part + " "
        else:
            formatted_d += line.strip() + "\n        "
            line = part + " "
    formatted_d += line.strip()

    # Update the 'd' attribute with the formatted string
    path_element.set("d", formatted_d)


def add_namespace_to_svg(file_path, namespace):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Define the namespace and update the root tag
        ET.register_namespace("", namespace)
        root.tag = "{" + namespace + "}" + root.tag

        # Format 'd' attributes
        for path_element in root.findall(".//{http://www.w3.org/2000/svg}path"):
            format_d_attribute(path_element)

        # Write the modified tree back to the file
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
    except ET.ParseError:
        print(f"Failed to parse {file_path}")


def process_directory(directory, namespace):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".svg"):
                file_path = os.path.join(subdir, file)
                print(f"Processing {file_path}")
                add_namespace_to_svg(file_path, namespace)


# Set your directory and namespace here
directory = "resources/images/arrows/pro"
namespace = "http://www.w3.org/2000/svg"

process_directory(directory, namespace)
