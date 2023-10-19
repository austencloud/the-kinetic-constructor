
import xml.etree.ElementTree as ET
from PyQt6.QtSvg import QSvgRenderer


class Svg_Manager():
    def __init__(self):
        self.renderers = {}

    @staticmethod
    def parse_svg_file(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for element in root.iter('{http://www.w3.org/2000/svg}path'):
            print('tag:', element.tag)
            print('attributes:', element.attrib)
            return element.attrib.get('d')

    @staticmethod
    def compare_svg_paths(file_path_1, file_path_2):
        tree_1 = ET.parse(file_path_1)
        root_1 = tree_1.getroot()

        tree_2 = ET.parse(file_path_2)
        root_2 = tree_2.getroot()

        path_data_1 = None
        for element in root_1.iter('{http://www.w3.org/2000/svg}path'):
            path_data_1 = element.attrib.get('d')
            break 

        path_data_2 = None
        for element in root_2.iter('{http://www.w3.org/2000/svg}path'):
            path_data_2 = element.attrib.get('d')
            break

        if path_data_1 == path_data_2:
            print('The SVG paths are identical.')
        else:
            print('The SVG paths are different.')


    @staticmethod
    def get_main_element_id(svg_file):
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Get the first element with an 'id' attribute
        for element in root.iter():
            if 'id' in element.attrib:
                return element.attrib['id']
        return None
    
    @staticmethod
    def point_in_svg(point, svg_file):
        svg_path = Svg_Manager.parse_svg_file(svg_file)
        qpainter_path = Svg_Manager.svg_path_to_qpainterpath(svg_path)
        return qpainter_path.contains(point)
    
    def get_renderer(self, filename):
        if filename not in self.renderers:
            self.renderers[filename] = QSvgRenderer(filename)
        return self.renderers[filename]
    
    def calculate_quadrant(start_position, end_position):
        if start_position == "n" and end_position == "e" or start_position == "e" and end_position == "n":
            return "ne"
        elif start_position == "n" and end_position == "w" or start_position == "w" and end_position == "n":
            return "nw"
        elif start_position == "s" and end_position == "e" or start_position == "e" and end_position == "s":
            return "se"
        elif start_position == "s" and end_position == "w" or start_position == "w" and end_position == "s":
            return "sw"
        # Add more conditions here if necessary

    def generate_pictograph_variations(self, arrow_combination):
        # Define the mappings for rotations and reflections
        rotation_mapping = {"n": "e", "e": "s", "s": "w", "w": "n"}
        vertical_reflection_mapping = {"n": "s", "s": "n", "e": "e", "w": "w"}
        horizontal_reflection_mapping = {"n": "n", "s": "s", "e": "w", "w": "e"}
        rotation_reflection_mapping = {"l": "r", "r": "l"}

        # Generate the rotated versions
        rotated_versions = [arrow_combination]
        for _ in range(3):
            arrow_combination = [{**arrow, 
                                "start_position": rotation_mapping[arrow["start_position"]],
                                "end_position": rotation_mapping[arrow["end_position"]],
                                "quadrant": self.calculate_quadrant(rotation_mapping[arrow["start_position"]], rotation_mapping[arrow["end_position"]])} 
                                for arrow in arrow_combination]
            rotated_versions.append(arrow_combination)

        # Generate the reflected versions
        reflected_versions = []
        for version in rotated_versions:
            vertical_reflected_version = [{**arrow, 
                                        "start_position": vertical_reflection_mapping[arrow["start_position"]],
                                        "end_position": vertical_reflection_mapping[arrow["end_position"]],
                                        "rotation": rotation_reflection_mapping[arrow["rotation"]],
                                        "quadrant": self.calculate_quadrant(vertical_reflection_mapping[arrow["start_position"]], vertical_reflection_mapping[arrow["end_position"]])} 
                                        for arrow in version]
            horizontal_reflected_version = [{**arrow, 
                                            "start_position": horizontal_reflection_mapping[arrow["start_position"]],
                                            "end_position": horizontal_reflection_mapping[arrow["end_position"]],
                                            "rotation": rotation_reflection_mapping[arrow["rotation"]],
                                            "quadrant": self.calculate_quadrant(horizontal_reflection_mapping[arrow["start_position"]], horizontal_reflection_mapping[arrow["end_position"]])} 
                                            for arrow in version]
            reflected_versions.extend([vertical_reflected_version, horizontal_reflected_version])

        return rotated_versions + reflected_versions

