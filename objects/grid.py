import json
from typing import TYPE_CHECKING, NamedTuple, Union, Literal
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsSceneWheelEvent, QGraphicsSceneMouseEvent
from PyQt6.QtCore import QPointF, QEvent
from data.constants import (
    BOX,
    DIAMOND,
)
from Enums.Enums import GridModes
from Enums.PropTypes import (
    strictly_placed_props,
)
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:

    from base_widgets.base_pictograph.base_pictograph import BasePictograph


GRID_DIR = "images/grid/"


class GridItem(QGraphicsSvgItem):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(100)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent | None) -> None:
        return super().wheelEvent(event)

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()


class GridPoint(NamedTuple):
    name: str
    coordinates: QPointF


class GridLayer:
    def __init__(self, points_data: dict[str, str]) -> None:
        self.points: dict[str, GridPoint] = {}
        for name, coords in points_data.items():
            if coords != "None":
                x, y = map(float, coords.strip("()").split(", "))
                self.points[name] = GridPoint(name, QPointF(x, y))
            else:
                self.points[name] = GridPoint(name, None)


class GridData:
    def __init__(self, data: dict[str, Union[str, dict[str, dict[str, str]]]]) -> None:
        self.hand_points_normal = GridLayer(data["hand_points"]["diamond"]["normal"])
        self.hand_points_strict = GridLayer(data["hand_points"]["diamond"]["strict"])
        self.layer2_points_normal = GridLayer(
            data["layer2_points"]["diamond"]["normal"]
        )
        self.layer2_points_strict = GridLayer(
            data["layer2_points"]["diamond"]["strict"]
        )
        self.outer_points = GridLayer(data["outer_points"])
        x, y = map(float, data["center_point"].strip("()").split(", "))
        self.center_point = GridPoint("center_point", QPointF(x, y))

    def get_point(self, layer: GridLayer, pos: QPointF) -> GridPoint:
        min_distance = float("inf")
        closest_point = None

        for point in layer.points.values():
            if point.coordinates is not None:
                distance = (pos - point.coordinates).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

        return closest_point


class Grid:
    def __init__(self, scene: "BasePictograph"):
        self.scene = scene
        self.items: dict[GridModes, GridItem] = {}
        self.layers: dict[str, GridItem] = {}
        self.grid_mode = DIAMOND
        self.grid_data = self._load_grid_data()
        self._create_grid_items(scene)
        self.center = self.grid_data.center_point.coordinates

    def hide(self):
        for item in self.items.values():
            item.setVisible(False)

    def toggle_non_radial_points_visibility(self, visible: bool):
        self.nonradial_layer.setVisible(visible)

    def _load_grid_data(self) -> GridData:
        json_path = get_images_and_data_path("data/circle_coords.json")
        with open(json_path, "r") as file:
            data = json.load(file)
        return GridData(data)

    def get_closest_hand_point(self, pos: QPointF) -> tuple[str, QPointF]:
        strict = self.scene.main_widget.prop_type in strictly_placed_props
        layer = (
            self.grid_data.hand_points_strict
            if strict
            else self.grid_data.hand_points_normal
        )
        closest_point = self.grid_data.get_point(layer, pos)
        return closest_point.name, closest_point.coordinates

    def get_closest_layer2_point(self, pos: QPointF) -> tuple[str, QPointF]:
        layer = self.grid_data.layer2_points_normal
        closest_point = self.grid_data.get_point(layer, pos)
        return closest_point.name, closest_point.coordinates

    def _create_grid_items(self, pictograph: "BasePictograph"):
        # Define paths for your grid images or components
        paths = {
            DIAMOND: get_images_and_data_path(f"{GRID_DIR}diamond_grid.svg"),
            BOX: get_images_and_data_path(f"{GRID_DIR}box_grid.svg"),
        }
        # Create grid items based on the mode and paths
        for mode, path in paths.items():
            grid_item = GridItem(path)
            pictograph.addItem(grid_item)
            grid_item.setVisible(mode == self.grid_mode)
            self.items[mode] = grid_item

        non_radial_path = get_images_and_data_path(
            f"{GRID_DIR}diamond_nonradial_points.svg"
        )
        non_radial_item = QGraphicsSvgItem(non_radial_path)
        non_radial_item.setVisible(False)  # Initially hidden
        self.scene.addItem(non_radial_item)
        self.nonradial_layer = non_radial_item

    def set_layer_visibility(self, layer_id, visibility):
        if layer_id in self.layers:
            self.layers[layer_id].setVisible(visibility)

    def toggle_layer_visibility(self, layer_id):
        if layer_id in self.layers:
            current_visibility = self.layers[layer_id].isVisible()
            self.layers[layer_id].setVisible(not current_visibility)

    def setPos(self, position: QPointF) -> None:
        for item in self.items.values():
            item.setPos(position)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        event.ignore()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        event.ignore()

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False
