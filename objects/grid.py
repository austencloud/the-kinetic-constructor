from xml.etree import ElementTree as ET
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from settings.numerical_constants import *
from settings.string_constants import *
from typing import Any


class Grid(QGraphicsSvgItem):
    def __init__(self, grid_svg_path) -> None:
        super().__init__(grid_svg_path)
        self.svg_file = grid_svg_path
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)

    def get_circle_coordinates(self, circle_id) -> QPointF | None:
        with open(self.svg_file, "r") as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        namespace = "{http://www.w3.org/2000/svg}"
        circle_element = root.find(f".//{namespace}circle[@id='{circle_id}']")
        if circle_element is not None:
            cx = float(circle_element.attrib["cx"])
            cy = float(circle_element.attrib["cy"])
            return QPointF(cx, cy)
        else:
            return None

    def init_points(self, point_names, constants) -> dict[str, QPointF]:
        return {
            constant: self.get_circle_coordinates(point_name)
            for point_name, constant in zip(point_names, constants)
        }

    def init_center(self) -> None:
        self.center: QPointF = self.get_circle_coordinates("center_point")

    def init_handpoints(self) -> None:
        point_names = ["n_hand_point", "e_hand_point", "s_hand_point", "w_hand_point"]
        constants = [NORTH, EAST, SOUTH, WEST]
        self.handpoints = self.init_points(point_names, constants)

    def init_layer2_points(self) -> None:
        point_names = [
            "ne_layer2_point",
            "se_layer2_point",
            "sw_layer2_point",
            "nw_layer2_point",
        ]
        constants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        self.layer2_points = self.init_points(point_names, constants)

    def mousePressEvent(self, event) -> None:
        pass

    def mouseMoveEvent(self, event) -> None:
        pass

    def mouseReleaseEvent(self, event) -> None:
        pass
