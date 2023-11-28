from typing import TYPE_CHECKING, Tuple

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import QPointF

from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.letter_item import LetterItem
from objects.props import Staff, Club, Fan, Hoop, Buugeng, Triad
from settings.string_constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    EAST,
    END_LOCATION,
    LAYER,
    LOCATION,
    MOTION_TYPE,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    PRO,
    PROP_TYPE,
    location,
    RED,
    ROTATION_DIRECTION,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    STAFF,
    START_LOCATION,
    TURNS,
    WEST,
    ORIENTATION,
    IN,
)
from widgets.graph_editor.pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class PictographInit:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.main_widget = pictograph.main_widget
        self.window_width = pictograph.main_widget.main_window.main_window_width
        self.window_height = pictograph.main_widget.main_window.main_window_height

    def init_view(self) -> QGraphicsView:
        view = PictographView(self.pictograph)
        return view

    def init_grid(self) -> Grid:
        grid = Grid("resources/images/grid/grid.svg")
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)
        self.pictograph.addItem(grid)
        grid.init_center()
        grid.init_handpoints()
        grid.init_layer2_points()
        self.pictograph.grid = grid
        return grid

    def init_prop_set(self) -> dict[str, Staff]:
        red_prop_dict = {COLOR: RED, LOCATION: NORTH, LAYER: 1, ORIENTATION: IN}
        blue_prop_dict = {COLOR: BLUE, LOCATION: SOUTH, LAYER: 1, ORIENTATION: IN}

        red_staff = Staff(self.pictograph, red_prop_dict)
        blue_staff = Staff(self.pictograph, blue_prop_dict)

        red_club = Club(self.pictograph, red_prop_dict)
        blue_club = Club(self.pictograph, blue_prop_dict)

        red_fan = Fan(self.pictograph, red_prop_dict)
        blue_fan = Fan(self.pictograph, blue_prop_dict)

        red_hoop = Hoop(self.pictograph, red_prop_dict)
        blue_hoop = Hoop(self.pictograph, blue_prop_dict)

        red_buugeng = Buugeng(self.pictograph, red_prop_dict)
        blue_buugeng = Buugeng(self.pictograph, blue_prop_dict)

        red_triad = Triad(self.pictograph, red_prop_dict)
        blue_triad = Triad(self.pictograph, blue_prop_dict)

        red_staff.set_svg_color(RED)
        blue_staff.set_svg_color(BLUE)

        red_staff.hide()
        blue_staff.hide()

        prop_set = {RED: red_staff, BLUE: blue_staff}
        return prop_set

    def init_ghost_arrows(self) -> dict[str, GhostArrow]:
        default_red_ghost_arrow_attributes = {
            COLOR: RED,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            LOCATION: NORTHEAST,
            START_LOCATION: NORTH,
            END_LOCATION: EAST,
            TURNS: 0,
        }

        default_blue_ghost_arrow_attributes = {
            COLOR: BLUE,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            LOCATION: SOUTHWEST,
            START_LOCATION: SOUTH,
            END_LOCATION: WEST,
            TURNS: 0,
        }

        red_ghost_arrow = GhostArrow(
            self.pictograph, default_red_ghost_arrow_attributes
        )
        blue_ghost_arrow = GhostArrow(
            self.pictograph, default_blue_ghost_arrow_attributes
        )

        ghost_arrows = {RED: red_ghost_arrow, BLUE: blue_ghost_arrow}
        return ghost_arrows

    def init_ghost_props(self) -> dict[str, GhostProp]:
        default_red_ghost_prop_attributes = {
            COLOR: RED,
            PROP_TYPE: STAFF,
            LOCATION: EAST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        default_blue_ghost_prop_attributes = {
            COLOR: BLUE,
            PROP_TYPE: STAFF,
            LOCATION: WEST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        red_ghost_prop = GhostProp(self.pictograph, default_red_ghost_prop_attributes)
        blue_ghost_prop = GhostProp(self.pictograph, default_blue_ghost_prop_attributes)

        ghost_props = {RED: red_ghost_prop, BLUE: blue_ghost_prop}
        return ghost_props

    def init_letter_item(self) -> QGraphicsSvgItem:
        letter_item = LetterItem(self.pictograph)
        self.pictograph.addItem(letter_item)
        letter_item.position_letter_item(letter_item)
        return letter_item

    def init_locations(self, grid: Grid) -> dict[str, Tuple[int, int, int, int]]:
        grid_center = grid.get_circle_coordinates("center_point").toPoint()

        grid_center_x = grid_center.x()
        grid_center_y = grid_center.y()

        ne_boundary = (
            grid_center_x,
            0,
            self.pictograph.width(),
            grid_center_y,
        )
        se_boundary = (
            grid_center_x,
            grid_center_y,
            self.pictograph.width(),
            self.pictograph.height(),
        )
        sw_boundary = (0, grid_center_y, grid_center_x, self.pictograph.height())
        nw_boundary = (
            0,
            0,
            grid_center_x,
            grid_center_y,
        )
        locations = {
            NORTHEAST: ne_boundary,
            SOUTHEAST: se_boundary,
            SOUTHWEST: sw_boundary,
            NORTHWEST: nw_boundary,
        }
        return locations
