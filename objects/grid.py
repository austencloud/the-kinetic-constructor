from xml.etree import ElementTree as ET
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


class Grid(QGraphicsSvgItem):
    def __init__(self, grid_svg_path):
        super().__init__(grid_svg_path)
        self.svg_file = grid_svg_path

    def get_circle_coordinates(self, circle_id):
        with open(self.svg_file, 'r') as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        namespace = '{http://www.w3.org/2000/svg}'
        circle_element = root.find(f".//{namespace}circle[@id='{circle_id}']")
        if circle_element is not None:
            cx = float(circle_element.attrib['cx'])
            cy = float(circle_element.attrib['cy'])
            return cx, cy
        else:
            return None

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass