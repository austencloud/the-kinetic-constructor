import json
from typing import TYPE_CHECKING, NamedTuple, Union, Literal
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsSceneWheelEvent, QGraphicsSceneMouseEvent
from PyQt6.QtCore import QPointF, QEvent
from constants import (
    BOX,
    DIAMOND,
    GRID_DIR,
)
from utilities.TypeChecking.TypeChecking import GridModes
from utilities.TypeChecking.prop_types import (
    strictly_placed_props,
)

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import (
        PropBox,
    )
    from widgets.pictograph.pictograph import Pictograph


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
    def __init__(self, scene: Union["ArrowBox", "PropBox", "Pictograph"]) -> None:
        self.scene = scene
        self.items: dict[GridModes, GridItem] = {}
        self.grid_mode = DIAMOND
        self.grid_data = self._load_grid_data()
        self._create_grid_items(scene)
        self.center = self.grid_data.center_point.coordinates

    def _load_grid_data(self) -> GridData:
        with open(
            "F:\\CODE\\tka-app\\tka-sequence-constructor\\data\\circle_coords.json", "r"
        ) as file:
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
        layer = (
            self.grid_data.layer2_points_normal
        )  # or layer2_points_strict based on some condition
        closest_point = self.grid_data.get_point(layer, pos)
        return closest_point.name, closest_point.coordinates

    def _create_grid_items(self, grid_scene: "Pictograph") -> None:
        paths = {
            DIAMOND: f"{GRID_DIR}diamond_grid.svg",
            BOX: f"{GRID_DIR}box_grid.svg",
        }

        for mode, path in paths.items():
            item = GridItem(path)
            grid_scene.addItem(item)
            self.items[mode] = item
            item.setVisible(mode == self.grid_mode)

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
