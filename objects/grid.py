from typing import List, Dict, Union
from xml.etree import ElementTree as ET
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


from settings.string_constants import (
    NORTH,
    EAST,
    SOUTH,
    WEST,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
)


class Grid(QGraphicsSvgItem):
    """
    Represents a grid object in the application.

    Args:
        grid_svg_path (str): The path to the SVG file for the grid.

    Attributes:
        svg_file (str): The path to the SVG file for the grid.
        center (QPointF): The coordinates of the center point of the grid.
        handpoints (Dict[str, QPointF]): A dictionary mapping hand point names to their coordinates.
        layer2_points (Dict[str, QPointF]): A dictionary mapping layer 2 point names to their coordinates.

    Methods:
        get_circle_coordinates: Get the coordinates of a circle in the SVG file.
        init_points: Initialize the points of the grid.
        init_center: Initialize the center point of the grid.
        init_handpoints: Initialize the hand points of the grid.
        init_layer2_points: Initialize the layer 2 points of the grid.
        mousePressEvent: Handle the mouse press event.
        mouseMoveEvent: Handle the mouse move event.
        mouseReleaseEvent: Handle the mouse release event.
    """

    def __init__(self, grid_svg_path: str) -> None:
        super().__init__(grid_svg_path)
        self.svg_file: str = grid_svg_path
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(-1)

    def get_circle_coordinates(self, circle_id: str) -> Union[QPointF, None]:
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

    def init_points(
        self, point_names: List[str], constants: List[str]
    ) -> Dict[str, QPointF]:
        return {
            constant: self.get_circle_coordinates(point_name)
            for point_name, constant in zip(point_names, constants)
        }

    def init_center(self) -> None:
        self.center: QPointF = self.get_circle_coordinates("center_point")

    def init_handpoints(self) -> None:
        point_names = ["n_hand_point", "e_hand_point", "s_hand_point", "w_hand_point"]
        constants = [NORTH, EAST, SOUTH, WEST]
        self.handpoints: Dict[str, QPointF] = self.init_points(point_names, constants)

    def init_layer2_points(self) -> None:
        point_names = [
            "ne_layer2_point",
            "se_layer2_point",
            "sw_layer2_point",
            "nw_layer2_point",
        ]
        constants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        self.layer2_points: Dict[str, QPointF] = self.init_points(
            point_names, constants
        )

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
