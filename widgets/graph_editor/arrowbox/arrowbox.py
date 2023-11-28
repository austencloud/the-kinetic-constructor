from typing import TYPE_CHECKING, List

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene, QGridLayout

from objects.arrow import Arrow
from settings.string_constants import (
    ANTI,
    ARROW_LOCATION,
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    EAST,
    END_LOCATION,
    MOTION_TYPE,
    NORTH,
    NORTHEAST,
    PRO,
    LOCATION,
    RED,
    ROTATION_DIRECTION,
    START_LOCATION,
    TURNS,
    SOUTHEAST,
    SOUTH,
    SOUTHWEST,
    NORTHWEST,
    WEST,
)
from widgets.graph_editor.arrowbox.arrowbox_drag import ArrowBoxDrag
from widgets.graph_editor.arrowbox.arrowbox_view import ArrowBoxView
from objects.grid import Grid

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from objects.arrow import Arrow

from utilities.TypeChecking.TypeChecking import MotionAttributesDicts


class ArrowBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.setSceneRect(0, 0, 750, 750)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = ArrowBoxView(self)

        self.populate_arrows()
        self.grid = Grid("resources/images/grid/grid_simple.svg")
        self.addItem(self.grid)
        self.grid.setPos(0, 0)
        self.target_arrow: "Arrow" = None
        self.arrowbox_layout = QGridLayout()
        self.arrowbox_layout.addWidget(self.view)
        self.arrowbox_drag = None

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

        for dict in red_arrow_attributes:
            arrow = Arrow(self, dict)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.arrows.append(arrow)
            self.red_arrows.append(arrow)

        for dict in blue_arrow_attributes:
            arrow = Arrow(self, dict)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.arrows.append(arrow)
            self.blue_arrows.append(arrow)

        for arrow in self.arrows:
            arrow.update_appearance()
            arrow.setTransformOriginPoint(arrow.boundingRect().center())
            arrow.is_dim(True)

        self.red_arrows[0].setPos(425, 50)  # RED PRO CLOCKWISE NE
        self.red_arrows[1].setPos(425, 425)  # RED PRO COUNTERCLOCKWISE SE
        self.red_arrows[2].setPos(375, 375)  # RED ANTI CLOCKWISE SE
        self.red_arrows[3].setPos(375, 100)  # RED ANTI COUNTERCLOCKWISE NE

        self.blue_arrows[0].setPos(50, 425)  # BLUE PRO CLOCKWISE SW
        self.blue_arrows[1].setPos(50, 50)  # BLUE PRO COUNTERCLOCKWISE NW
        self.blue_arrows[2].setPos(100, 100)  # BLUE ANTI CLOCKWISE NW
        self.blue_arrows[3].setPos(100, 375)  # BLUE ANTI COUNTERCLOCKWISE SW

    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        # Find the closest arrow to the cursor position
        closest_arrow = None
        min_distance = float("inf")
        for arrow in self.arrows:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance

        # Proceed only if the closest arrow is found
        if closest_arrow:
            self.target_arrow = closest_arrow
            if not self.arrowbox_drag:
                pictograph = self.main_widget.graph_editor.pictograph
                self.arrowbox_drag = ArrowBoxDrag(self.main_window, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.arrowbox_drag.match_target_arrow(self.target_arrow)
                self.arrowbox_drag.start_drag(event_pos)
        else:
            # If no closest arrow is found, ignore the event
            self.target_arrow = None
            event.ignore()

    def mouseMoveEvent(self, event) -> None:
        if self.target_arrow and self.arrowbox_drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.arrowbox_drag.handle_mouse_move(event_pos)
        else:
            cursor_pos = event.scenePos()
            closest_arrow = None
            min_distance = float("inf")

            for arrow in self.arrows:
                arrow_center = arrow.sceneBoundingRect().center()
                distance = (
                    cursor_pos - arrow_center
                ).manhattanLength()  # Manhattan distance for simplicity

                if distance < min_distance:
                    closest_arrow = arrow
                    min_distance = distance

            for arrow in self.arrows:
                if arrow != closest_arrow:
                    arrow.is_dim(True)  # Highlight all arrows except the closest one
                else:
                    arrow.is_dim(False)  # Do not highlight the closest one

    def mouseReleaseEvent(self, event) -> None:
        if self.arrowbox_drag:
            self.arrowbox_drag.handle_mouse_release()
            self.target_arrow = None  # Reset

        # After releasing, highlight the arrow under the cursor
        cursor_pos = event.scenePos()
        closest_arrow = None
        min_distance = float("inf")

        for arrow in self.arrows:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (cursor_pos - arrow_center).manhattanLength()

            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance

        # Update the dim state of each arrow
        for arrow in self.arrows:
            if arrow != closest_arrow:
                arrow.is_dim(True)
            else:
                arrow.is_dim(False)

    def dim_all_arrows(self) -> None:
        for arrow in self.arrows:
            arrow.is_dim(True)
