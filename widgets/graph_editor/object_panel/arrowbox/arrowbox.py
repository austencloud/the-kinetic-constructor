from typing import TYPE_CHECKING, List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QGridLayout
from objects.arrow.arrow import Arrow
from constants.string_constants import *
from widgets.graph_editor.object_panel.arrowbox.arrowbox_drag import ArrowBoxDrag
from widgets.graph_editor.object_panel.arrowbox.arrowbox_view import ArrowBoxView
from objects.grid import Grid
from widgets.graph_editor.object_panel.objectbox import ObjectBox
from utilities.TypeChecking.TypeChecking import MotionAttributesDicts
from PyQt6.QtCore import QPointF
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


class ArrowBox(ObjectBox):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__(main_widget, graph_editor)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.view = ArrowBoxView(self, graph_editor)
        self.grid = Grid(self)
        self.target_arrow: "Arrow" = None
        self.drag = None

        self.populate_arrows()

        self.arrowbox_layout = QGridLayout()
        self.arrowbox_layout.addWidget(self.view)

    def populate_arrows(self) -> None:
        self.arrows: List[Arrow] = []
        self.red_arrows: List[Arrow] = []
        self.blue_arrows: List[Arrow] = []

    def populate_arrows(self) -> None:
        self.arrows: List[Arrow] = []
        self.red_arrows: List[Arrow] = []
        self.blue_arrows: List[Arrow] = []

        red_arrow_attributes: List[MotionAttributesDicts] = [
            {
                COLOR: RED,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
        ]

        blue_arrow_attributes: List[MotionAttributesDicts] = [
            {
                COLOR: BLUE,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
        ]
        red_arrow_positions: List[Tuple[int, int]] = [
            (425, 50),
            (425, 425),
            (375, 375),
            (375, 100),
        ]
        blue_arrow_positions: List[Tuple[int, int]] = [
            (50, 425),
            (50, 50),
            (100, 100),
            (100, 375),
        ]

        self.create_arrows_for_color(RED, self.red_arrows, red_arrow_attributes)
        self.create_arrows_for_color(BLUE, self.blue_arrows, blue_arrow_attributes)

        self.position_arrows(self.red_arrows, red_arrow_positions)
        self.position_arrows(self.blue_arrows, blue_arrow_positions)

    def create_arrows_for_color(self, color: str, arrow_list: List[Arrow], attributes: List[MotionAttributesDicts]) -> None:
        for attr in attributes:
            arrow = Arrow(self, attr, self.pictograph.motions[color])
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            arrow_list.append(arrow)
            self.arrows.append(arrow)
            arrow.update_appearance()
            arrow.setTransformOriginPoint(arrow.boundingRect().center())
            arrow.is_dim(True)

    def position_arrows(self, arrows: List[Arrow], positions: List[Tuple[int, int]]) -> None:
        for arrow, pos in zip(arrows, positions):
            arrow.setPos(*pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)
        closest_arrow = self.find_closest_arrow(scene_pos)

        if closest_arrow:
            self.target_arrow = closest_arrow
            if not self.drag:
                pictograph = self.main_widget.graph_editor_widget.graph_editor.pictograph
                self.drag = ArrowBoxDrag(self.main_window, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag.match_target_arrow(self.target_arrow)
                self.drag.start_drag(event_pos)
        else:
            self.target_arrow = None
            event.ignore()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.target_arrow and self.drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.drag.handle_mouse_move(event_pos)
        else:
            self.highlight_closest_arrow(event.scenePos())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.drag:
            self.drag.handle_mouse_release()
            self.target_arrow = None
        self.highlight_closest_arrow(event.scenePos())

    def find_closest_arrow(self, scene_pos: QPointF) -> "Arrow":
        closest_arrow = None
        min_distance = float("inf")
        for arrow in self.arrows:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance
        return closest_arrow

    def highlight_closest_arrow(self, cursor_pos: QPointF) -> None:
        closest_arrow = self.find_closest_arrow(cursor_pos)
        for arrow in self.arrows:
            arrow.is_dim(arrow != closest_arrow)

    def dim_all_arrows(self) -> None:
        for arrow in self.arrows:
            arrow.is_dim(True)