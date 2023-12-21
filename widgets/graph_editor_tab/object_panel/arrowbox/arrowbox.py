from typing import TYPE_CHECKING, List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QGridLayout
from objects.arrow.arrow import Arrow
from constants.string_constants import *
from objects.motion import Motion
from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox_drag import ArrowBoxDrag
from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox_view import ArrowBoxView
from objects.grid import Grid
from widgets.graph_editor_tab.object_panel.objectbox import ObjectBox
from utilities.TypeChecking.TypeChecking import MotionAttributesDicts
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor import GraphEditor


class ArrowBox(ObjectBox):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__(main_widget, graph_editor)
        self.main_widget = main_widget
        self.view = ArrowBoxView(self, graph_editor)
        self.grid = Grid(self)
        self.target_arrow: "Arrow" = None
        self.drag = None
        self.default_start_orientation = IN
        self.start_orientation = self.default_start_orientation
        self.motions: List[Motion] = self.create_motions()
        self.arrows: List[Arrow] = self.create_arrows()

        self.arrowbox_layout = QGridLayout()
        self.arrowbox_layout.addWidget(self.view)

    def create_arrows(self) -> None:
        red_arrows: List[Arrow] = []
        blue_arrows: List[Arrow] = []
        arrows: List[Arrow] = []
        for motion in self.motions:
            arrow_dict = {
                COLOR: motion.color,
                MOTION_TYPE: motion.motion_type,
                TURNS: motion.turns,
            }

            arrow = Arrow(self, arrow_dict, motion)
            motion.arrow = arrow
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            arrows.append(arrow)
            if arrow.color == RED:
                red_arrows.append(arrow)
            elif arrow.color == BLUE:
                blue_arrows.append(arrow)
            arrow.setTransformOriginPoint(arrow.boundingRect().center())
            arrow.is_dim(True)

        red_arrow_positions: List[Tuple[int, int]] = [
            (525, 150),
            (525, 525),
            (475, 475),
            (475, 200),
        ]
        blue_arrow_positions: List[Tuple[int, int]] = [
            (150, 525),
            (150, 150),
            (200, 200),
            (200, 475),
        ]

        self.position_arrows(red_arrows, red_arrow_positions)
        self.position_arrows(blue_arrows, blue_arrow_positions)

        for motion in self.motions:
            motion.arrow.location = motion.get_arrow_location(
                motion.start_location, motion.end_location
            )

        for arrow in arrows:
            arrow.update_appearance()
            arrow.update_rotation()

        return arrows

    def create_motions(self) -> None:
        motions = []
        motion_dicts: List[MotionAttributesDicts] = [
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: RED,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                ARROW_LOCATION: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
            {
                COLOR: BLUE,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                ARROW_LOCATION: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
                START_ORIENTATION: IN,
                START_LAYER: 1,
            },
        ]

        for motion_dict in motion_dicts:
            motion = Motion(self, motion_dict)
            motions.append(motion)
        return motions

    def position_arrows(
        self, arrows: List[Arrow], positions: List[Tuple[int, int]]
    ) -> None:
        for arrow, pos in zip(arrows, positions):
            arrow.setPos(*pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)
        closest_arrow = self.find_closest_arrow(scene_pos)

        if closest_arrow:
            self.target_arrow = closest_arrow
            if not self.drag:
                pictograph = (
                    self.main_widget.graph_editor_tab.graph_editor.main_pictograph
                )
                self.drag = ArrowBoxDrag(self.main_widget, pictograph, self)
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
