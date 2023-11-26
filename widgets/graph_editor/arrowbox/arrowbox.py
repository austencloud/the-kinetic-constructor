from typing import TYPE_CHECKING, List

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene, QGridLayout

from objects.arrow import Arrow
from settings.string_constants import (
    ANTI,
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
    QUADRANT,
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

from utilities.TypeChecking.TypeChecking import ArrowAttributesDicts


class ArrowBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.setSceneRect(0, 0, 750, 750)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.setup_view()
        self.populate_arrows()
        self.grid = Grid("resources/images/grid/grid_simple.svg")
        self.addItem(self.grid)
        self.grid.setPos(0, 0)
        self.target_arrow: "Arrow" = None
        self.arrowbox_layout = QGridLayout()
        self.arrowbox_layout.addWidget(self.view)
        self.arrowbox_drag = None

    def setup_view(self) -> None:
        view = ArrowBoxView(self)
        self.view = view

    def populate_arrows(self) -> None:
        self.arrows: List[Arrow] = []
        initial_arrow_attribute_collection: List[ArrowAttributesDicts] = [
            {
                COLOR: RED,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                QUADRANT: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                QUADRANT: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                QUADRANT: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                QUADRANT: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: CLOCKWISE,
                QUADRANT: SOUTHEAST,
                START_LOCATION: SOUTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: RED,
                MOTION_TYPE: ANTI,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                QUADRANT: NORTHEAST,
                START_LOCATION: NORTH,
                END_LOCATION: EAST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: CLOCKWISE,
                QUADRANT: SOUTHWEST,
                START_LOCATION: SOUTH,
                END_LOCATION: WEST,
                TURNS: 0,
            },
            {
                COLOR: BLUE,
                MOTION_TYPE: PRO,
                ROTATION_DIRECTION: COUNTER_CLOCKWISE,
                QUADRANT: NORTHWEST,
                START_LOCATION: NORTH,
                END_LOCATION: WEST,
                TURNS: 0,
            }
        ]

        for dict in initial_arrow_attribute_collection:
            arrow = Arrow(self, dict)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.addItem(arrow)
            self.arrows.append(arrow)

        for arrow in self.arrows:
            arrow.update_appearance()
            arrow.setTransformOriginPoint(arrow.boundingRect().center())
            arrow.is_dim(True)

        self.arrows[0].setPos(425, 50) # RED PRO CLOCKWISE NE
        self.arrows[1].setPos(100, 375) # BLUE ANTI COUNTERCLOCKWISE SW
        
        self.arrows[2].setPos(425, 425) # RED PRO COUNTERCLOCKWISE SE
        self.arrows[3].setPos(100, 100) # BLUE ANTI CLOCKWISE NW
        
        self.arrows[4].setPos(375, 375) # RED ANTI CLOCKWISE SE
        self.arrows[5].setPos(375, 100) # RED ANTI COUNTERCLOCKWISE NE
        
        self.arrows[6].setPos(50, 425) # BLUE PRO CLOCKWISE SW
        self.arrows[7].setPos(50, 50) # BLUE PRO COUNTERCLOCKWISE NW

    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        arrows = [item for item in self.items(scene_pos) if isinstance(item, Arrow)]

        closest_arrow = None
        min_distance = float('inf')
        for arrow in arrows:
            arrow_center = arrow.sceneBoundingRect().center()
            distance = (scene_pos - arrow_center).manhattanLength()
            if distance < min_distance:
                closest_arrow = arrow
                min_distance = distance

        if closest_arrow:
            self.target_arrow = closest_arrow
            if not self.arrowbox_drag:
                graphboard = self.main_widget.graph_editor.graphboard
                self.arrowbox_drag = ArrowBoxDrag(self.main_window, graphboard, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.arrowbox_drag.match_target_arrow(self.target_arrow)
                self.arrowbox_drag.start_drag(event_pos)
        else:
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
            min_distance = float('inf')

            for arrow in self.arrows:
                arrow_center = arrow.sceneBoundingRect().center()
                distance = (cursor_pos - arrow_center).manhattanLength()  # Manhattan distance for simplicity

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
            
    def onMouseLeaveScene(self) -> None:
        # Redim all arrows when the mouse leaves the scene
        for arrow in self.arrows:
            arrow.is_dim(True)