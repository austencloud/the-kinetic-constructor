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
        self.grid_mode = DIAMOND

        self.items = {}

        self._init_all_points(grid_scene)
        self._init_center()
        self._init_hand_points()
        self._init_layer2_points()

        if self.grid_mode == DIAMOND:
            self.hide_box_mode_elements()
        elif self.grid_mode == BOX:
            self.hide_diamond_mode_elements()

    ### INITIALIZATION ###

    def init_points(
        self, point_names: List[str], constants: List[str]
    ) -> Dict[str, QPointF]:
        return {
            constant: self.get_circle_coordinates(point_name)
            for point_name, constant in zip(point_names, constants)
        }

    def _init_center(self) -> None:
        self.center: QPointF = self.get_circle_coordinates("center_point")

    def _init_hand_points(self) -> None:
        diamond_hand_point_names = [
            "n_hand_point",
            "e_hand_point",
            "s_hand_point",
            "w_hand_point",
        ]
        diamond_hand_point_constants = [NORTH, EAST, SOUTH, WEST]
        self.diamond_hand_points: Dict[str, QPointF] = self.init_points(
            diamond_hand_point_names, diamond_hand_point_constants
        )

        box_hand_point_names = [
            "ne_hand_point",
            "se_hand_point",
            "sw_hand_point",
            "nw_hand_point",
        ]
        box_hand_point_constants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        self.box_hand_points: Dict[str, QPointF] = self.init_points(
            box_hand_point_names, box_hand_point_constants
        )

    def _init_layer2_points(self) -> None:
        diamond_layer2_point_names = [
            "ne_layer2_point",
            "se_layer2_point",
            "sw_layer2_point",
            "nw_layer2_point",
        ]
        diamond_layer2_constants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        self.diamond_layer2_points: Dict[str, QPointF] = self.init_points(
            diamond_layer2_point_names, diamond_layer2_constants
        )

        box_layer2_point_names = [
            "n_layer2_point",
            "e_layer2_point",
            "s_layer2_point",
            "w_layer2_point",
        ]
        box_layer2_constants = [NORTH, EAST, SOUTH, WEST]
        self.box_layer2_points: Dict[str, QPointF] = self.init_points(
            box_layer2_point_names, box_layer2_constants
        )

    def _init_all_points(
        self, grid_scene: Union["ArrowBox", "PropBox", "Pictograph"]
    ) -> None:
        self.diamond_svg_paths = {
            "center_point": f"{GRID_DIR}grid_center_point.svg",
            "diamond_hand_points": f"{GRID_DIR}diamond/grid_diamond_hand_points.svg",
            "diamond_layer2_points": f"{GRID_DIR}diamond/grid_diamond_layer2_points.svg",
            "diamond_outer_points": f"{GRID_DIR}diamond/grid_diamond_outer_points.svg",
        }

        self.box_svg_paths = {
            "center_point": f"{GRID_DIR}grid_center_point.svg",
            "box_hand_points": f"{GRID_DIR}box/grid_box_hand_points.svg",
            "box_layer2_points": f"{GRID_DIR}box/grid_box_layer2_points.svg",
            "box_outer_points": f"{GRID_DIR}box/grid_box_outer_points.svg",
        }

        center_item = GridItem(self.diamond_svg_paths["center_point"])
        grid_scene.addItem(center_item)
        self.items["center_point"] = center_item

        for key, path in self.diamond_svg_paths.items():
            if key != "center_point":
                item = GridItem(path)
                grid_scene.addItem(item)
                self.items[key] = item

        for key, path in self.box_svg_paths.items():
            if key != "center_point":
                item = GridItem(path)
                grid_scene.addItem(item)
                box_key = f"box_{key}"
                self.items[box_key] = item

    def init_outer_points(self) -> None:
        # Initialize the outer points similarly to how hand_points and layer2_points are initialized
        pass

    def setPos(self, position: QPointF) -> None:
        for item in self.items.values():
            item.setPos(position)

    def scale_grid(self, scale_factor: float) -> None:
        # Determine the center point of the grid layout before scaling
        grid_center = QPointF(self.grid_scene.width() / 2, self.grid_scene.height() / 2)

        for item in self.items.values():
            item.setTransform(QTransform())

            item_center = item.boundingRect().center()
            transform = QTransform()
            transform.translate(item_center.x(), item_center.y())
            transform.scale(scale_factor, scale_factor)
            transform.translate(-item_center.x(), -item_center.y())
            item.setTransform(transform)

            relative_pos = (item.pos() - grid_center) * scale_factor
            new_pos = grid_center + relative_pos - item_center * scale_factor
            item.setPos(new_pos)

    ### TOGGLES ###

    def toggle_element_visibility(self, element_id: str, visible: bool):
        if element_id in self.items:
            self.items[element_id].setVisible(visible)
        else:
            print(f"Warning: Element with id '{element_id}' not found.")

    def toggle_grid_mode(self, grid_mode: GridModes) -> None:
        self.grid_mode = grid_mode

    def hide_box_mode_elements(self) -> None:
        for key in self.box_svg_paths:
            if key != "center_point":  # Exclude the center point as it's common
                box_key = f"box_{key}"
                self.toggle_element_visibility(box_key, False)

    def hide_diamond_mode_elements(self) -> None:
        for key in self.diamond_svg_paths:
            if key != "center_point":  # Exclude the center point as it's common
                self.toggle_element_visibility(key, False)

    ### GETTERS ###

    def get_circle_coordinates_from_path(self, path_d: str) -> QPointF:
        # Extract the coordinates from the path's 'd' attribute
        path_parts = path_d.split(" ")
        if path_parts[0] == "M":
            center_x = float(path_parts[1])
            center_y = float(path_parts[2])
            return QPointF(center_x, center_y)
        return QPointF()

    def get_circle_coordinates(self, circle_id: str) -> Union[QPointF, None]:
        svg_file_path = self._get_svg_file_path(circle_id)

        if not svg_file_path:
            return None

        with open(svg_file_path, "r") as svg_file:
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


    def _get_svg_file_path(self, circle_id: str) -> str:
        if "hand" in circle_id:
            if any(x in circle_id for x in ["ne_", "se_", "sw_", "nw_"]):
                return self.box_svg_paths["box_hand_points"]
            else:
                return self.diamond_svg_paths["diamond_hand_points"]
        elif "layer2" in circle_id: 
            if any(x in circle_id for x in ["ne_", "se_", "sw_", "nw_"]):
                return self.diamond_svg_paths["diamond_layer2_points"]
            else:
                return self.box_svg_paths["box_layer2_points"]
        elif "outer" in circle_id:
            if any(x in circle_id for x in ["ne_", "se_", "sw_", "nw_"]):
                return self.box_svg_paths["box_outer_points"]
            else:
                return self.diamond_svg_paths["diamond_outer_points"]
        elif "center" in circle_id:
            return self.diamond_svg_paths["center_point"]
        return ""

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()
