from typing import TYPE_CHECKING, List, Dict, Union
from xml.etree import ElementTree as ET
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtGui import QTransform

from settings.string_constants import (
    BOX,
    DIAMOND,
    GRID_DIR,
    NORTH,
    EAST,
    SOUTH,
    WEST,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
)
from utilities.TypeChecking.TypeChecking import GridModes

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class GridItem(QGraphicsSvgItem):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(-1)

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()


class Grid:
    def __init__(self, grid_scene: Union["ArrowBox", "PropBox", "Pictograph"]) -> None:
        self.grid_mode: GridModes = DIAMOND
        self.items: Dict[str, GridItem] = {}
        self._initialize_grid_elements(grid_scene)
        self._apply_grid_mode(self.grid_mode)

    def _initialize_grid_elements(
        self, grid_scene: Union["ArrowBox", "PropBox", "Pictograph"]
    ) -> None:
        self.center = self.get_circle_coordinates("center_point")
        self.diamond_hand_points = self._init_points(
            [
                "n_diamond_hand_point",
                "e_diamond_hand_point",
                "s_diamond_hand_point",
                "w_diamond_hand_point",
            ],
            [NORTH, EAST, SOUTH, WEST],
        )
        self.box_hand_points = self._init_points(
            [
                "ne_box_hand_point",
                "se_box_hand_point",
                "sw_box_hand_point",
                "nw_box_hand_point",
            ],
            [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
        )
        self.diamond_layer2_points = self._init_points(
            [
                "ne_diamond_layer2_point",
                "se_diamond_layer2_point",
                "sw_diamond_layer2_point",
                "nw_diamond_layer2_point",
            ],
            [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
        )
        self.box_layer2_points = self._init_points(
            [
                "n_box_layer2_point",
                "e_box_layer2_point",
                "s_box_layer2_point",
                "w_box_layer2_point",
            ],
            [NORTH, EAST, SOUTH, WEST],
        )
        self._create_grid_items(grid_scene)

    def _create_grid_items(self, grid_scene: "Pictograph") -> None:
        # Updated paths to include the whole SVG for each grid mode
        paths = {
            DIAMOND: f"{GRID_DIR}diamond_grid.svg",
            BOX: f"{GRID_DIR}box_grid.svg",
        }

        for mode, path in paths.items():
            item = GridItem(path)
            grid_scene.addItem(item)
            self.items[mode] = item

    def _init_points(
        self, point_names: List[str], constants: List[str]
    ) -> Dict[str, QPointF]:
        return {
            constant: self.get_circle_coordinates(point_name)
            for point_name, constant in zip(point_names, constants)
        }

    def _apply_grid_mode(self, grid_mode: GridModes) -> None:
        self.toggle_grid_mode(grid_mode)

    def _toggle_visibility(self, prefix: str, visible: bool) -> None:
        for key in self.items.keys():
            if key.startswith(prefix):
                self.items[key].setVisible(visible)

    def _hide_box_mode_elements(self) -> None:
        self.items[BOX].setVisible(False)

    def _hide_diamond_mode_elements(self) -> None:
        self.items[DIAMOND].setVisible(False)

    def get_circle_coordinates(self, circle_id: str) -> Union[QPointF, None]:
        svg_file_path = self._get_svg_file_path(circle_id)
        with open(svg_file_path, "r") as svg_file:
            svg_content = svg_file.read()

        root = ET.fromstring(svg_content)
        circle_element = root.find(
            f".//{{http://www.w3.org/2000/svg}}circle[@id='{circle_id}']"
        )
        if circle_element is not None:
            cx = float(circle_element.attrib["cx"])
            cy = float(circle_element.attrib["cy"])
            return QPointF(cx, cy)
        return None

    def _get_svg_file_path(self, circle_id: str) -> str:
        # Determine the correct SVG file based on the grid mode and circle ID
        if "diamond" in circle_id or "center_point" in circle_id:
            return f"{GRID_DIR}diamond_grid.svg"
        elif "box" in circle_id:
            return f"{GRID_DIR}box_grid.svg"
        # Fallback if no matching pattern is found

        return ""

    def setPos(self, position: QPointF) -> None:
        for item in self.items.values():
            item.setPos(position)

    def scale_grid(self, scale_factor: float) -> None:
        grid_center = QPointF(self.grid_scene.width() / 2, self.grid_scene.height() / 2)
        for item in self.items.values():
            item.setTransform(QTransform())
            item_center = item.boundingRect().center()
            transform = (
                QTransform()
                .translate(item_center.x(), item_center.y())
                .scale(scale_factor, scale_factor)
                .translate(-item_center.x(), -item_center.y())
            )
            item.setTransform(transform)
            relative_pos = (item.pos() - grid_center) * scale_factor
            item.setPos(grid_center + relative_pos - item_center * scale_factor)

    def toggle_element_visibility(self, element_id: str, visible: bool) -> None:
        if element_id in self.items:
            self.items[element_id].setVisible(visible)

    def toggle_grid_mode(self, grid_mode: GridModes) -> None:
        self.grid_mode = grid_mode
        if grid_mode == DIAMOND:
            self._hide_box_mode_elements()
        elif grid_mode == BOX:
            self._hide_diamond_mode_elements()

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
