import os
import xml.etree.ElementTree as ET

def simplify_svg(svg_file):
    # Parse the SVG file without namespaces
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Remove unnecessary attributes from the root <svg> element
    for attrib in ["version", "id", "xmlns:xlink", "x", "y", "style", "xml:space"]:
        if attrib in root.attrib:
            del root.attrib[attrib]

    # Find and remove the <style> element
    for style in root.findall('.//{http://www.w3.org/2000/svg}style'):
        root.remove(style)

    # Extract color from style and apply directly to each <path>
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        if "class" in path.attrib:
            # Assuming .st0 is always the class name and the color is always #2E3192
            path.attrib["fill"] = "#2E3192"
            del path.attrib["class"]
        if "id" in path.attrib:
            del path.attrib["id"]

    # Remove all group <g> tags but keep their children
    for group in root.findall('.//{http://www.w3.org/2000/svg}g'):
        root.extend(group)
        root.remove(group)

    # Write the changes back to the file
    tree.write(svg_file, xml_declaration=False)

def simplify_svgs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.svg'):
            file_path = os.path.join(directory, filename)
            simplify_svg(file_path)
            print(f"Simplified {filename}")

# Replace with your directory path
directory_path = 'C:/Users/Austen/Desktop/tka-app-backup-for-Be/tka-sequence-constructor/resources/images/arrows/pro'
simplify_svgs_in_directory(directory_path)
