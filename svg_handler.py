import os
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QPainterPath
from PyQt5.QtSvg import QSvgRenderer
from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Close


class Svg_Handler:
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
    def get_id_from_file(file):
        return os.path.splitext(os.path.basename(file))[0]

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
    def svg_path_to_qpainterpath(svg_path):
        qpainter_path = QPainterPath()
        for segment in svg_path:
            if isinstance(segment, Line):
                qpainter_path.lineTo(segment.end.real, segment.end.imag)
            elif isinstance(segment, CubicBezier):
                qpainter_path.cubicTo(segment.control1.real, segment.control1.imag,
                                    segment.control2.real, segment.control2.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, QuadraticBezier):
                qpainter_path.quadTo(segment.control.real, segment.control.imag,
                                    segment.end.real, segment.end.imag)
            elif isinstance(segment, Arc):
                # QPainterPath doesn't support arcs, so we need to approximate the arc with cubic beziers
                # This is a complex task and might require a separate function
                pass
            elif isinstance(segment, Close):
                qpainter_path.closeSubpath()
        return qpainter_path

    @staticmethod
    def get_main_element_id(svg_file):
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Get the first element with an 'id' attribute
        for element in root.iter():
            if 'id' in element.attrib:
                return element.attrib['id']
        return None
    
        
    def point_in_svg(self, point, svg_file):
        qpainter_path = self.svg_path_to_qpainterpath(svg_file)
        if qpainter_path is None:
            print(f"Warning: No QPainterPath found for SVG file {svg_file}")
            return False
        return qpainter_path.contains(point)
    
    def get_renderer(self, filename):
        if filename not in self.renderers:
            self.renderers[filename] = QSvgRenderer(filename)
        return self.renderers[filename]
    
