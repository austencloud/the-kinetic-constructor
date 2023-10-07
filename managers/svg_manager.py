import os
import json
import os
import xml.etree.ElementTree as ET
import json
import re
from PyQt5.QtGui import QImage, QPainter, QPainterPath, QTransform
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QMenu, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Close
from objects.arrow import Arrow
from objects.staff import Staff
from grid import Grid
from lxml import etree
from copy import deepcopy

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
    
