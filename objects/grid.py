import logging
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

GRID_DIR = "images/grid/"


from typing import Optional
from PyQt6.QtCore import QPointF


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
            logger.warning(f"Shift point '{point_name}' not found or has no coordinates.")
            return None

    def get_static_coord(self, point_name: str) -> Optional[QPointF]:
        """
        Retrieves the coordinates for a given static point name.
        """
        point = self.all_hand_points_normal.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:
            logger.warning(f"Static point '{point_name}' not found or has no coordinates.")
            return None

    def get_point(self, layer: dict[str, GridPoint], pos: QPointF) -> Optional[GridPoint]:
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
    def __init__(self, pictograph: "BasePictograph", grid_data: GridData, grid_mode: str):
        self.pictograph = pictograph
        self.grid_data = grid_data
        self.grid_mode = grid_mode  # Store the current grid mode
        self.items: dict[str, GridItem] = {}
        self.center = self.grid_data.center_points.get(grid_mode, QPointF(0, 0))  # Retrieve the center point

        if self.center == QPointF(0, 0):
            logger.warning(f"Center point for grid mode '{grid_mode}' not found. Using default (0,0).")

        self._create_grid_items()

    def _create_grid_items(self):
        """
        Create grid items for all grid modes.
        """
        paths = {
            "diamond": f"{GRID_DIR}diamond_grid.svg",
            "box": f"{GRID_DIR}box_grid.svg",
            # Add more grid modes and their paths as needed
        }

        for mode, path in paths.items():
            grid_item = GridItem(path)
            self.pictograph.addItem(grid_item)
            grid_item.setVisible(mode == self.grid_mode)  # Show only the current grid mode
            self.items[mode] = grid_item

        # Load non-radial points specific to the grid mode
        non_radial_paths = {
            "diamond": f"{GRID_DIR}diamond_nonradial_points.svg",
            "box": f"{GRID_DIR}box_nonradial_points.svg",
            # Add more grid modes and their non-radial paths as needed
        }
        non_radial_path = non_radial_paths.get(self.grid_mode)
        if non_radial_path:
            non_radial_item = QGraphicsSvgItem(non_radial_path)
            non_radial_item.setVisible(False)  # Initially hidden
            self.pictograph.addItem(non_radial_item)
            self.items[f"{self.grid_mode}_nonradial"] = non_radial_item

    def set_layer_visibility(self, layer_id: str, visibility: bool):
        """
        Sets visibility for a specific layer.
        """
        if layer_id in self.items:
            self.items[layer_id].setVisible(visibility)
        else:
            logger.warning(f"Layer '{layer_id}' not found.")

    def toggle_layer_visibility(self, layer_id: str):
        """
        Toggles visibility for a specific layer.
        """
        if layer_id in self.items:
            current_visibility = self.items[layer_id].isVisible()
            self.items[layer_id].setVisible(not current_visibility)
        else:
            logger.warning(f"Layer '{layer_id}' not found.")

    def setPos(self, position: QPointF) -> None:
        """
        Sets the position for all grid items.
        """
        for item in self.items.values():
            item.setPos(position)

    def get_closest_hand_point(self, pos: QPointF, strict: bool) -> Optional[GridPoint]:
        """
        Retrieves the closest hand point to the given position.
        """
        layer = (
            self.grid_data.all_hand_points_strict
            if strict
            else self.grid_data.all_hand_points_normal
        )
        closest_point = self.grid_data.get_point(layer, pos)
        return closest_point

    def get_closest_layer2_point(self, pos: QPointF) -> Optional[GridPoint]:
        """
        Retrieves the closest layer2 point to the given position.
        """
        closest_point = self.grid_data.get_point(self.grid_data.all_layer2_points, pos)
        return closest_point

    def toggle_non_radial_points_visibility(self, visible: bool):
        """
        Toggles visibility for non-radial points.
        """
        non_radial_key = f"{self.grid_mode}_nonradial"
        if non_radial_key in self.items:
            self.items[non_radial_key].setVisible(visible)
        else:
            logger.warning(f"Non-radial layer '{non_radial_key}' not found.")

    def hide(self):
        """
        Hides all grid items.
        """
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
