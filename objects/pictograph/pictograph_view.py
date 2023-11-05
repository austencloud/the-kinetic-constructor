from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QMenu
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsItem, QFrame
from PyQt6.QtGui import QTransform, QAction
from objects.grid import Grid
from objects.arrow.arrow import Arrow
from objects.pictograph.pictograph_staff_handler import PictographStaffHandler
from objects.arrow.arrow_manager import ArrowManager
from utilities.json_handler import JsonHandler
from widgets.graph_editor.graphboard.graphboard_info_handler import (
    GraphboardInfoHandler,
)
from resources.constants.constants import (
    PICTOGRAPH_WIDTH,
    PICTOGRAPH_HEIGHT,
    PICTOGRAPH_SCALE,
    PICTOGRAPH_GRID_PADDING,
)
from resources.constants.string_constants import COLOR, RED, BLUE, STATIC, PRO, ANTI

class PictographView(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        self.setup_view()
        self.main_widget = main_widget
        self.pictograph_scene = QGraphicsScene()
        self.setScene(self.pictograph_scene)
        self.init_grid()
        self.init_handlers_and_managers()
        self.init_staffs()
        self.infobox = None

    def setup_view(self):
        self.setFixedSize(PICTOGRAPH_WIDTH, PICTOGRAPH_HEIGHT)
        self.view_scale = PICTOGRAPH_SCALE
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def init_handlers_and_managers(self):
        self.info_handler = GraphboardInfoHandler(self.main_widget, self)
        self.staff_handler = PictographStaffHandler(
            self.main_widget, self.pictograph_scene
        )
        self.arrow_manager = ArrowManager(self.main_widget)
        self.json_handler = JsonHandler(self.pictograph_scene)
        self.staff_handler.connect_pictograph_view(self)
        self.staff_handler.connect_grid(self.grid)
        self.staff_factory = self.staff_handler.factory

    def init_staffs(self):
        self.staff_handler.init_handpoints(self, self.grid)
        self.staff_handler.initializer.init_staffs(self)

    def init_grid(self):
        self.grid = Grid("resources/images/grid/grid.svg")
        self.grid.setScale(PICTOGRAPH_SCALE)
        self.pictograph_scene.addItem(self.grid)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.adjust_item_positions()

    def adjust_item_positions(self):
        for item in self.pictograph_scene.selectedItems():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable:
                self.keep_item_within_bounds(item)

    def keep_item_within_bounds(self, item):
        rect = item.sceneBoundingRect()
        sceneRect = self.pictograph_sceneRect()
        if not sceneRect.contains(rect):
            item_x = min(sceneRect.right(), max(rect.left(), sceneRect.left()))
            item_y = min(sceneRect.bottom(), max(rect.top(), sceneRect.top()))
            item.setPos(QPointF(item_x, item_y))

    def get_state(self):
        state = {
            "arrows": [],
        }
        for item in self.pictograph_scene.items():
            if isinstance(item, Arrow):
                state["arrows"].append(
                    {
                        COLOR: item.color,
                        "motion_type": item.motion_type,
                        "rotation_direction": item.rotation_direction,
                        "quadrant": item.quadrant,
                        "start_location": item.start_location,
                        "end_location": item.end_location,
                        "turns": item.turns,
                    }
                )
        return state

    def get_quadrant_center(self, quadrant):
        # Calculate the layer 2 points on the graphboard based on the grid
        graphboard_layer2_points = {}
        for point_name in [
            "NE_layer2_point",
            "SE_layer2_point",
            "SW_layer2_point",
            "NW_layer2_point",
        ]:
            cx, cy = self.grid.get_circle_coordinates(point_name)
            graphboard_layer2_points[point_name] = QPointF(cx, cy)

        # Map the quadrants to the corresponding layer 2 points
        centers = {
            "ne": graphboard_layer2_points["NE_layer2_point"],
            "se": graphboard_layer2_points["SE_layer2_point"],
            "sw": graphboard_layer2_points["SW_layer2_point"],
            "nw": graphboard_layer2_points["NW_layer2_point"],
        }

        return centers.get(quadrant, QPointF(0, 0))

    def get_arrows(self):
        # return the current arrows on the graphboard as an array
        current_arrows = []
        for arrow in self.pictograph_scene().items():
            if isinstance(arrow, Arrow):
                current_arrows.append(arrow)
        return current_arrows

    def populate_pictograph(self, combination):
        DISTANCE = 40 * PICTOGRAPH_SCALE
        created_arrows = []
        optimal_locations = next(
            (
                d
                for d in combination
                if "optimal_red_location" in d and "optimal_blue_location" in d
            ),
            None,
        )
        for arrow_dict in combination:
            if all(
                key in arrow_dict
                for key in [
                    COLOR,
                    "motion_type",
                    "rotation_direction",
                    "quadrant",
                    "turns",
                ]
            ):
                if (
                    arrow_dict["motion_type"] == PRO
                    or arrow_dict["motion_type"] == ANTI
                ):
                    self.place_shift_arrows(
                        DISTANCE, created_arrows, optimal_locations, arrow_dict
                    )

                elif arrow_dict["motion_type"] == STATIC:
                    self.place_ghost_arrows(created_arrows, arrow_dict)

        for arrow in created_arrows:
            if arrow not in self.pictograph_scene.items():
                self.pictograph_scene.addItem(arrow)
        self.staff_handler.update_pictograph_staffs(self.pictograph_scene)

    def place_ghost_arrows(self, created_arrows, arrow_dict):
        ghost_arrow = self.arrow_manager.arrow_factory.create_arrow(self, arrow_dict)

        created_arrows.append(ghost_arrow)

    def place_shift_arrows(
        self, DISTANCE, created_arrows, optimal_locations, arrow_dict
    ):
        arrow = self.arrow_manager.factory.create_arrow(self, arrow_dict)

        arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        created_arrows.append(arrow)

        for arrow in created_arrows:
            # Calculate the center of the bounding rectangle
            center = arrow.boundingRect().center()

            if optimal_locations:
                optimal_location = optimal_locations.get(
                    f"optimal_{arrow.color}_location"
                )
                if optimal_location:
                    # Adjust the position based on the center
                    pos = (
                        QPointF(
                            optimal_location["x"] * PICTOGRAPH_SCALE,
                            optimal_location["y"] * PICTOGRAPH_SCALE,
                        )
                        - center * PICTOGRAPH_SCALE
                    )
                    new_pos = pos + QPointF(0, 0)
                    arrow.setPos(new_pos)
            else:
                quadrant_center = self.get_quadrant_center(arrow.quadrant)
                pos = quadrant_center * PICTOGRAPH_SCALE
                pos = (pos + QPointF(0, 0)) - (arrow.center * PICTOGRAPH_SCALE)
                if arrow.quadrant == "ne":
                    pos += QPointF(DISTANCE, -DISTANCE)
                elif arrow.quadrant == "se":
                    pos += QPointF(DISTANCE, DISTANCE)
                elif arrow.quadrant == "sw":
                    pos += QPointF(-DISTANCE, DISTANCE)
                elif arrow.quadrant == "nw":
                    pos += QPointF(-DISTANCE, -DISTANCE)
                arrow.setPos(
                    pos + QPointF(PICTOGRAPH_GRID_PADDING, PICTOGRAPH_GRID_PADDING)
                )

    def save_optimal_positions(self):
        MAIN_GRAPHBOARD_BUFFER = (
            self.graphboard_view.width()
            - self.graphboard_view.grid.boundingRect().width()
        ) / 2
        MAIN_GRAPHBOARD_V_OFFSET = (
            self.graphboard_view.height() - self.graphboard_view.width()
        ) / 2

        for item in self.pictograph_scene.items():
            if isinstance(item, Arrow):
                pos = item.pos() + item.boundingRect().center() * PICTOGRAPH_SCALE
                # Reverse the scaling
                pos = pos / PICTOGRAPH_SCALE
                # Reverse the vertical buffer
                pos.setY(pos.y() + MAIN_GRAPHBOARD_V_OFFSET)
                # Reverse the buffer
                pos = pos + QPointF(MAIN_GRAPHBOARD_BUFFER, MAIN_GRAPHBOARD_BUFFER)
                if item.get_attributes()[COLOR] == RED:
                    red_position = pos
                elif item.get_attributes()[COLOR] == BLUE:
                    blue_position = pos
        self.json_handler.update_optimal_locations_in_json(red_position, blue_position)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        saveOptimalAction = QAction("Save Optimal Positions", self)
        saveOptimalAction.triggered.connect(self.save_optimal_positions)
        contextMenu.addAction(saveOptimalAction)
        contextMenu.exec(event.globalPos())
