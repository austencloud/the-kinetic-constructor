from PyQt5.QtCore import QPointF
from xml.dom import minidom
from PyQt5.QtSvg import QGraphicsSvgItem

class Grid(QGraphicsSvgItem):

    def __init__(self, grid_svg, ui_setup):
        super().__init__(grid_svg)

        self.doc = minidom.parse(grid_svg)

        circles = self.doc.getElementsByTagName('circle')

        center_point_circle = None
        for circle in circles:
            if circle.getAttribute('id') == "center_point":
                center_point_circle = circle
                break
        if center_point_circle is None:
            raise ValueError("No circle with id 'center_point' found in SVG file")

        center_x = float(center_point_circle.getAttribute('cx'))
        center_y = float(center_point_circle.getAttribute('cy'))

        self.center_point = QPointF(center_x, center_y)

        # add an attribute svg_file to the grid
        self.svg_file = grid_svg

    def updateSvgContent(self, svg_content):
        self.setSharedRenderer(svg_content)

    def scale_for_4k(self):
        print("scale_for_4k")
        self.setScale(1.0)
        
    def scale_for_2400x1600(self):
        print("scale_for_2400x1600")
        self.setScale(0.5)

    def getCenter(self):
        return self.mapToScene(self.center_point)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass