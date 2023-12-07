from typing import TYPE_CHECKING, Dict, Tuple

from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import QPointF

from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.letter_item import LetterItem
from objects.prop import Prop, Staff, Club, Fan, Hoop, Buugeng, Triad
from settings.string_constants import *
from utilities.TypeChecking.TypeChecking import Colors, Locations, PropTypes
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
        grid = Grid(self.pictograph)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)
        grid.init_center()
        grid.init_handpoints()
        grid.init_layer2_points()
        self.pictograph.grid = grid
        return grid

    def init_prop_set(self, prop_type: PropTypes) -> Dict[Colors, Prop]:
        red_prop_Dict = {
            COLOR: RED,
            PROP_TYPE: prop_type,
            PROP_LOCATION: NORTH,
            LAYER: 1,
            ORIENTATION: IN,
        }
        blue_prop_Dict = {
            COLOR: BLUE,
            PROP_TYPE: prop_type,
            PROP_LOCATION: SOUTH,
            LAYER: 1,
            ORIENTATION: IN,
        }

        prop_class_mapping = {
            STAFF.lower(): Staff,
            CLUB.lower(): Club,
            FAN.lower(): Fan,
            HOOP.lower(): Hoop,
            BUUGENG.lower(): Buugeng,
            TRIAD.lower(): Triad
        }

        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")

        red_prop: Prop = prop_class(self.pictograph, red_prop_Dict)
        blue_prop: Prop = prop_class(self.pictograph, blue_prop_Dict)

        red_prop.set_svg_color(RED)
        blue_prop.set_svg_color(BLUE)

        prop_set = {RED: red_prop, BLUE: blue_prop}
        return prop_set

    def init_ghost_arrows(self) -> Dict[Colors, GhostArrow]:
        default_red_ghost_arrow_attributes = {
            COLOR: RED,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            ARROW_LOCATION: NORTHEAST,
            START_LOCATION: NORTH,
            END_LOCATION: EAST,
            TURNS: 0,
        }

        default_blue_ghost_arrow_attributes = {
            COLOR: BLUE,
            MOTION_TYPE: PRO,
            ROTATION_DIRECTION: CLOCKWISE,
            ARROW_LOCATION: SOUTHWEST,
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

    def init_ghost_props(self, prop_type: PropTypes) -> Dict[Colors, GhostProp]:
    
        prop_class_mapping = {
            STAFF.lower(): Staff,
            CLUB.lower(): Club,
            FAN.lower(): Fan,
            HOOP.lower(): Hoop,
            BUUGENG.lower(): Buugeng,
            TRIAD.lower(): Triad
        }

        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")

        
        default_red_ghost_prop_attributes = {
            COLOR: RED,
            PROP_TYPE: prop_type,
            PROP_LOCATION: EAST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        default_blue_ghost_prop_attributes = {
            COLOR: BLUE,
            PROP_TYPE: prop_type,
            PROP_LOCATION: WEST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        red_ghost_prop = GhostProp(self.pictograph, default_red_ghost_prop_attributes)
        blue_ghost_prop = GhostProp(self.pictograph, default_blue_ghost_prop_attributes)

        ghost_props = {RED: red_ghost_prop, BLUE: blue_ghost_prop}
        return ghost_props

    def init_letter_item(self) -> LetterItem:
        letter_item = LetterItem(self.pictograph)
        self.pictograph.addItem(letter_item)
        letter_item.position_letter_item(letter_item)
        return letter_item

    def init_locations(self, grid: Grid) -> Dict[Locations, Tuple[int, int, int, int]]:
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

    def update_prop_set_and_ghost_props(self, new_prop_type: PropTypes) -> None:
        self.pictograph.prop_set = self.init_prop_set(new_prop_type)
        self.pictograph.prop_type = new_prop_type
        self.pictograph.ghost_props = self.init_ghost_props(new_prop_type)
