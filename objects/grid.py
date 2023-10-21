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

    def get_circle_radius(self, circle_id):
        with open(self.svg_file, 'r') as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        namespace = '{http://www.w3.org/2000/svg}'
        circle_element = root.find(f".//{namespace}circle[@id='{circle_id}']")
        if circle_element is not None:
            r = float(circle_element.attrib['r'])
            return r
        else:
            return None

    def add_red_dot(self, x, y):
        with open(self.svg_file, 'r') as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        namespace = '{http://www.w3.org/2000/svg}'
        red_dot = ET.Element(f"{namespace}circle")
        red_dot.attrib['cx'] = str(x)
        red_dot.attrib['cy'] = str(y)
        red_dot.attrib['r'] = '5'
        red_dot.attrib['fill'] = 'red'
        red_dot.attrib['stroke'] = 'black'
        red_dot.attrib['stroke-width'] = '1'
        root.append(red_dot)
        return ET.tostring(root)

    def get_width(self):
        return self.boundingRect().width() * self.scale()

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass