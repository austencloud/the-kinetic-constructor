from typing import TYPE_CHECKING, Tuple

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import QPointF

from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_staff import GhostStaff
from objects.grid import Grid
from objects.letter_item import LetterItem
from objects.staff import BlueStaff, RedStaff, Staff
from settings.numerical_constants import GRAPHBOARD_HEIGHT, GRAPHBOARD_WIDTH
from settings.string_constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    EAST,
    END_LOCATION,
    GRID_FILE_PATH,
    LAYER,
    LOCATION,
    MOTION_TYPE,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    PRO,
    QUADRANT,
    RED,
    ROTATION_DIRECTION,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    START_LOCATION,
    TURNS,
    WEST,
)
from widgets.graph_editor.graphboard.graphboard_view import GraphBoardView

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard


class GraphBoardInit:
    def __init__(self, graphboard: "GraphBoard") -> None:
        self.graphboard = graphboard
        self.main_widget = graphboard.main_widget
        self.window_width = graphboard.main_widget.main_window.main_window_width
        self.window_height = graphboard.main_widget.main_window.main_window_height

    def init_view(self) -> QGraphicsView:
        view = GraphBoardView(self.graphboard)
        return view

    def init_grid(self) -> Grid:
        grid = Grid(GRID_FILE_PATH)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)
        self.graphboard.addItem(grid)
        grid.init_center()
        grid.init_handpoints()
        grid.init_layer2_points()
        self.graphboard.grid = grid
        return grid

    def init_staff_set(self) -> dict[str, Staff]:
        red_staff_dict = {
            COLOR: RED,
            LOCATION: NORTH,
            LAYER: 1,
        }
        blue_staff_dict = {
            COLOR: BLUE,
            LOCATION: SOUTH,
            LAYER: 1,
        }

        red_staff = RedStaff(self.main_widget, self.graphboard, red_staff_dict)
        blue_staff = BlueStaff(self.main_widget, self.graphboard, blue_staff_dict)

        red_staff.hide()
        blue_staff.hide()

        staff_set = {RED: red_staff, BLUE: blue_staff}
        return staff_set

    def init_ghost_arrows(self) -> dict[str, GhostArrow]:
        default_red_ghost_arrow_attributes = {
            COLOR: RED,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            QUADRANT: NORTHEAST,
            START_LOCATION: NORTH,
            END_LOCATION: EAST,
            TURNS: 0,
        }

        default_blue_ghost_arrow_attributes = {
            COLOR: BLUE,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            QUADRANT: SOUTHWEST,
            START_LOCATION: SOUTH,
            END_LOCATION: WEST,
            TURNS: 0,
        }

        red_ghost_arrow = GhostArrow(
            self.graphboard, default_red_ghost_arrow_attributes
        )
        blue_ghost_arrow = GhostArrow(
            self.graphboard, default_blue_ghost_arrow_attributes
        )

        ghost_arrows = {RED: red_ghost_arrow, BLUE: blue_ghost_arrow}
        return ghost_arrows

    def init_ghost_staffs(self) -> dict[str, GhostStaff]:
        default_red_ghost_staff_attributes = {
            COLOR: RED,
            LOCATION: EAST,
            LAYER: 1,
        }

        default_blue_ghost_staff_attributes = {
            COLOR: BLUE,
            LOCATION: WEST,
            LAYER: 1,
        }

        red_ghost_staff = GhostStaff(
            self.main_widget, self.graphboard, default_red_ghost_staff_attributes
        )
        blue_ghost_staff = GhostStaff(
            self.main_widget, self.graphboard, default_blue_ghost_staff_attributes
        )

        ghost_staffs = {RED: red_ghost_staff, BLUE: blue_ghost_staff}
        return ghost_staffs

    def init_letter_item(self) -> QGraphicsSvgItem:
        letter_item = LetterItem(self.graphboard)
        self.graphboard.addItem(letter_item)
        self.graphboard.position_letter_item(letter_item)
        return letter_item

    def init_quadrants(self, grid: Grid) -> dict[str, Tuple[int, int, int, int]]:
        grid_center = grid.get_circle_coordinates("center_point").toPoint()

        grid_center_x = grid_center.x()
        grid_center_y = grid_center.y()

        ne_boundary = (
            grid_center_x,
            0,
            GRAPHBOARD_WIDTH,
            grid_center_y,
        )
        se_boundary = (
            grid_center_x,
            grid_center_y,
            GRAPHBOARD_WIDTH,
            GRAPHBOARD_HEIGHT,
        )
        sw_boundary = (
            0,
            grid_center_y,
            grid_center_x,
            GRAPHBOARD_HEIGHT,
        )
        nw_boundary = (
            0,
            0,
            grid_center_x,
            grid_center_y,
        )
        quadrants = {
            NORTHEAST: ne_boundary,
            SOUTHEAST: se_boundary,
            SOUTHWEST: sw_boundary,
            NORTHWEST: nw_boundary,
        }
        return quadrants