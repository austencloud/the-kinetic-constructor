from typing import TYPE_CHECKING, Dict, Tuple
from PyQt6.QtCore import QPointF
from Enums import (
    Color,
    MotionType,
    PropType,
)
from objects.arrow.arrow import Arrow
from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.letter_item import LetterItem
from objects.motion import Motion
from objects.prop.prop import Prop
from constants import *
from utilities.TypeChecking.TypeChecking import Location
from objects.prop.prop_types import *

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class PictographInit:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.main_widget = pictograph.main_widget

    ### INIT ###

    def init_grid(self) -> Grid:
        grid = Grid(self.pictograph)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)

        self.pictograph.grid = grid
        return grid

    def init_motions(self) -> Dict[Color, Motion]:
        return {color: self.create_motion(color) for color in [RED, BLUE]}

    def init_objects(self, prop_type: PropType) -> None:
        self.init_grid()
        self.pictograph.motions = self.init_motions()
        self.pictograph.arrows, self.pictograph.ghost_arrows = self.init_arrows()
        self.pictograph.props, self.pictograph.ghost_props = self.init_props(prop_type)

    def init_arrows(self) -> Tuple[Dict[Color, Arrow], Dict[Color, GhostArrow]]:
        arrows = {}
        ghost_arrows = {}
        for color in [BLUE, RED]:
            arrows[color], ghost_arrows[color] = self.create_arrow(color, PRO)
        return arrows, ghost_arrows

    def init_props(
        self, prop_type: PropType
    ) -> Tuple[Dict[Color, Prop], Dict[Color, GhostProp]]:
        props = {}
        ghost_props = {}
        for color in [RED, BLUE]:
            props[color], ghost_props[color] = self.create_prop(color, prop_type)
        return props, ghost_props

    def init_letter_item(self) -> LetterItem:
        letter_item = LetterItem(self.pictograph)
        self.pictograph.addItem(letter_item)
        return letter_item

    def init_locations(self, grid: Grid) -> Dict[Location, Tuple[int, int, int, int]]:
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

    ### CREATE ###

    def create_arrow(
        self, color: Color, motion_type: MotionType
    ) -> Tuple[Arrow, GhostArrow]:
        arrow_attributes = {
            COLOR: color,
            MOTION_TYPE: motion_type,
            TURNS: 0,
        }
        arrow = Arrow(self.pictograph, arrow_attributes, None)
        ghost_arrow = GhostArrow(self.pictograph, arrow_attributes, None)
        return arrow, ghost_arrow

    def create_prop(self, color: Color, prop_type: PropType) -> Tuple[Prop, GhostProp]:
        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")
        prop_attributes = {
            COLOR: color,
            PROP_TYPE: prop_type,
            LOCATION: None,
            ORIENTATION: None,
        }
        prop: Prop = prop_class(self.pictograph, prop_attributes, None)
        prop.set_svg_color(color)
        ghost_prop = GhostProp(
            self.pictograph, prop_attributes, self.pictograph.motions[color]
        )
        return prop, ghost_prop

    def create_motion(self, color: Color) -> Motion:
        motion_dict = {
            COLOR: color,
            ARROW: None,
            PROP: None,
            MOTION_TYPE: None,
            PROP_ROT_DIR: None,
            TURNS: 0,
            START_LOC: None,
            END_LOC: None,
            START_OR: None,
        }
        return Motion(self.pictograph, motion_dict, blank=True)


prop_class_mapping = {
    STAFF: Staff,
    BIGSTAFF: BigStaff,
    CLUB: Club,
    FAN: Fan,
    BIGFAN: BigFan,
    MINIHOOP: MiniHoop,
    BUUGENG: Buugeng,
    BIGBUUGENG: BigBuugeng,
    FRACTALGENG: Fractalgeng,
    TRIAD: Triad,
    BIGTRIAD: BigTriad,
    DOUBLESTAR: DoubleStar,
    BIGHOOP: BigHoop,
    BIGDOUBLESTAR: BigDoubleStar,
    QUIAD: Quiad,
    SWORD: Sword,
    GUITAR: Guitar,
    UKULELE: Ukulele,
    CHICKEN: Chicken,
}
