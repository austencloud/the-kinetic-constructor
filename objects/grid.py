import logging
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from main_window.settings_manager.visibility_settings.grid_visibility_manager import (
        GridVisibilityManager,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

GRID_DIR = "images/grid/"


from typing import Optional
from PyQt6.QtCore import QPointF

from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import QPointF, Qt


import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QGraphicsItemGroup


class NonRadialGridPoints(QGraphicsItemGroup):
    child_points: list[QGraphicsEllipseItem] = []
    name = "non_radial_points"
    
    def __init__(self, path, visibility_manager):
        super().__init__()
        self.visibility_manager = visibility_manager
        self._parse_svg(path)

    def _parse_svg(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        namespace = {"": "http://www.w3.org/2000/svg"}

        non_radial_group = root.find(".//*[@id='non_radial_points']", namespace)
        if not non_radial_group:
            print(f"Group 'non_radial_points' not found in {path}")
            return

        for circle in non_radial_group.findall("circle", namespace):
            cx = float(circle.attrib.get("cx", 0))
            cy = float(circle.attrib.get("cy", 0))
            r = float(circle.attrib.get("r", 0))
            point_id = circle.attrib.get("id", "unknown_point")
            point = NonRadialPoint(cx, cy, r, point_id, self.visibility_manager)
            point.setParentItem(self)
            self.child_points.append(point)


class NonRadialPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, r, point_id, visibility_manager: "GridVisibilityManager"):
        super().__init__(-r, -r, 2 * r, 2 * r)
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setPos(QPointF(x, y))
        self.setAcceptHoverEvents(True)
        self.setToolTip(point_id)
        self.point_id = point_id
        self.visibility_manager = visibility_manager
        self.setZValue(101)

    def hoverEnterEvent(self, event):
        if self._is_near(event.pos()):
            self.setBrush(QBrush(QColor("yellow")))

    def hoverLeaveEvent(self, event):
        visible = self.visibility_manager.non_radial_visible
        self.setBrush(QBrush(QColor("black" if visible else "gray")))

    def mousePressEvent(self, event):
        if self._is_near(event.pos()):
            self.visibility_manager.toggle_non_radial_points_visibility()
            visible = self.visibility_manager.non_radial_visible
            self.setBrush(QBrush(QColor("black" if visible else "gray")))

    def _is_near(self, pos):
        """Check if the cursor is close enough to the center."""
        distance = (pos - self.boundingRect().center()).manhattanLength()
        return distance <= self.boundingRect().width() / 2


class GridPoint:
    def __init__(self, name: str, coordinates: Optional[QPointF]) -> None:
        self.name = name
        self.coordinates = coordinates


class GridLayer:
    def __init__(self, points_data: dict[str, str]) -> None:
        self.points: dict[str, GridPoint] = {}
        for name, coords in points_data.items():
            if coords != "None":
                try:
                    x, y = map(float, coords.strip("()").split(", "))
                    self.points[name] = GridPoint(name, QPointF(x, y))
                except ValueError:
                    print(f"Warning: Invalid coordinates for point '{name}'.")
                    self.points[name] = GridPoint(name, None)
            else:
                self.points[name] = GridPoint(name, None)


class GridData:
    def __init__(self, data: dict[str, dict[str, dict[str, str]]]) -> None:
        """
        Initializes GridData by loading all points from all grid modes.
        """
        self.all_layer2_points: dict[str, GridPoint] = {}
        self.all_hand_points_normal: dict[str, GridPoint] = {}
        self.all_hand_points_strict: dict[str, GridPoint] = {}
        self.all_layer2_points_strict: dict[str, GridPoint] = {}
        self.all_outer_points: dict[str, GridPoint] = {}
        self.center_points: dict[str, QPointF] = {}

        for mode, mode_data in data.items():
            # Load Layer 2 Normal Points
            layer2_normal = GridLayer(mode_data["layer2_points"]["normal"])
            self.all_layer2_points.update(layer2_normal.points)

            # Load Layer 2 Strict Points
            layer2_strict = GridLayer(mode_data["layer2_points"]["strict"])
            self.all_layer2_points_strict.update(layer2_strict.points)

            # Load Hand Points Normal
            hand_normal = GridLayer(mode_data["hand_points"]["normal"])
            self.all_hand_points_normal.update(hand_normal.points)

            # Load Hand Points Strict
            hand_strict = GridLayer(mode_data["hand_points"]["strict"])
            self.all_hand_points_strict.update(hand_strict.points)

            # Load Outer Points
            outer_points = GridLayer(mode_data["outer_points"])
            self.all_outer_points.update(outer_points.points)

            # Load Center Point
            center_coords = mode_data.get("center_point", "None")
            if center_coords != "None":
                try:
                    x, y = map(float, center_coords.strip("()").split(", "))
                    self.center_points[mode] = QPointF(x, y)
                except ValueError:
                    print(
                        f"Warning: Invalid center point coordinates for mode '{mode}'."
                    )
                    self.center_points[mode] = QPointF(0, 0)  # Default center point
            else:
                print(
                    f"Warning: Center point missing for mode '{mode}'. Using default."
                )
                self.center_points[mode] = QPointF(0, 0)  # Default center point

    def get_shift_coord(self, point_name: str) -> Optional[QPointF]:
        """
        Retrieves the coordinates for a given layer2 point name.
        """
        point = self.all_layer2_points.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:
            logger.warning(
                f"Shift point '{point_name}' not found or has no coordinates."
            )
            return None

    def get_static_coord(self, point_name: str) -> Optional[QPointF]:
        """
        Retrieves the coordinates for a given static point name.
        """
        point = self.all_hand_points_normal.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:
            logger.warning(
                f"Static point '{point_name}' not found or has no coordinates."
            )
            return None

    def get_point(
        self, layer: dict[str, GridPoint], pos: QPointF
    ) -> Optional[GridPoint]:
        """
        Returns the closest point to the given position within the specified layer.
        """
        min_distance = float("inf")
        closest_point = None
        for point in layer.values():
            if point.coordinates:
                distance = (pos - point.coordinates).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point
        if not closest_point:
            logger.warning("No closest point found.")
        return closest_point


class GridItem(QGraphicsSvgItem):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(100)

    def wheelEvent(self, event) -> None:
        event.ignore()

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()


logger = logging.getLogger(__name__)

GRID_DIR = "images/grid/"


class Grid:
    def __init__(
        self, pictograph: "BasePictograph", grid_data: GridData, grid_mode: str
    ):
        self.pictograph = pictograph
        self.grid_data = grid_data
        self.grid_mode = grid_mode
        self.items: dict[str, GridItem] = {}
        self.center = self.grid_data.center_points.get(grid_mode, QPointF(0, 0))

        if self.center == QPointF(0, 0):
            logger.warning(
                f"Center point for grid mode '{grid_mode}' not found. Using default (0,0)."
            )

        self._create_grid_items()

    def _create_grid_items(self):
        paths = {
            "diamond": f"{GRID_DIR}diamond_grid.svg",
            "box": f"{GRID_DIR}box_grid.svg",
        }

        for mode, path in paths.items():
            grid_item = GridItem(path)
            self.pictograph.addItem(grid_item)
            grid_item.setVisible(mode == self.grid_mode)
            self.items[mode] = grid_item

        non_radial_paths = {
            "diamond": f"{GRID_DIR}diamond_nonradial_points.svg",
            "box": f"{GRID_DIR}box_nonradial_points.svg",
        }

        non_radial_path = non_radial_paths.get(self.grid_mode)
        if non_radial_path:
            non_radial_points = NonRadialGridPoints(
                non_radial_path, self.pictograph.main_widget.settings_manager.visibility
            )
            self.pictograph.addItem(non_radial_points)
            self.items[f"{self.grid_mode}_nonradial"] = non_radial_points

    def toggle_non_radial_points_visibility(self, visible: bool):
        non_radial_key = f"{self.grid_mode}_nonradial"
        if non_radial_key in self.items:
            self.items[non_radial_key].setVisible(visible)
        else:
            logger.warning(f"Non-radial layer '{non_radial_key}' not found.")

    def hide(self):
        for item in self.items.values():
            item.setVisible(False)

    def update_grid_mode(self):
        grid_mode = self.pictograph.main_widget.grid_mode_checker.get_grid_mode(
            self.pictograph.pictograph_dict
        )
        self.pictograph.grid.hide()
        self.pictograph.grid.__init__(
            self.pictograph, self.pictograph.grid.grid_data, grid_mode
        )
