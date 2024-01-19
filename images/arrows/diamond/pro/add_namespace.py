from lxml import etree
import os

def format_d_attribute(path_element, line_length=80):
    d_attr = path_element.get('d')
    if not d_attr:
        return

    formatted_d = ""
    line = ""
    for part in d_attr.split():
        if len(line) + len(part) < line_length:
            line += part + " "
        else:
            formatted_d += line.strip() + "\n        "
            line = part + " "
    formatted_d += line.strip()

    path_element.set('d', formatted_d)

def add_namespace_to_svg(file_path, namespace):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()

        root.set("xmlns", namespace)

        for path_element in root.xpath('//svg:path', namespaces={"svg": "http://www.w3.org/2000/svg"}):
            format_d_attribute(path_element)

        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    except etree.XMLSyntaxError as e:
        print(f"Failed to parse {file_path}: {e}")

def process_directory(directory, namespace):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.svg'):
                file_path = os.path.join(subdir, file)
                print(f"Processing {file_path}")
                add_namespace_to_svg(file_path, namespace)

# Set your directory and namespace here
directory = "images/arrows"
namespace = "http://www.w3.org/2000/svg"

process_directory(directory, namespace)

