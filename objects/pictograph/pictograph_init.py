from typing import TYPE_CHECKING, Dict, Tuple

from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow

from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.letter_item import LetterItem
from objects.motion import Motion
from objects.prop.prop_types import *
from constants.string_constants import *
from utilities.TypeChecking.TypeChecking import Colors, Locations, PropTypes

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class PictographInit:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.main_widget = pictograph.main_widget


    def init_grid(self) -> Grid:
        grid = Grid(self.pictograph)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)

        self.pictograph.grid = grid
        return grid

    def init_motions(self) -> Dict[Colors, Motion]:
        motions = {}
        for color in [RED, BLUE]:
            motion_dict = {
                COLOR: color,
                ARROW: None,
                PROP: None,
                GHOST_ARROW: None,
                GHOST_PROP: None,
                MOTION_TYPE: None,
                ROTATION_DIRECTION: None,
                TURNS: 0,
                START_LOCATION: None,
                END_LOCATION: None,
                START_ORIENTATION: None,
                START_LAYER: 1,
            }

            motion = Motion(self.pictograph, motion_dict)
            motions[color] = motion
        return motions

    def init_arrows(self) -> Dict[Colors, Arrow]:
        default_red_arrow_attributes = {
            COLOR: RED,
            MOTION_TYPE: PRO,
            TURNS: 0,
        }

        default_blue_arrow_attributes = {
            COLOR: BLUE,
            MOTION_TYPE: PRO,
            TURNS: 0,
        }

        red_arrow = Arrow(
            self.pictograph,
            default_red_arrow_attributes,
            None,
        )
        blue_arrow = Arrow(
            self.pictograph,
            default_blue_arrow_attributes,
            None,
        )

        arrows = {RED: red_arrow, BLUE: blue_arrow}
        for motion in self.pictograph.motions.values():
            for arrow in arrows.values():
                if arrow.color == motion.color:
                    motion.arrow = arrow
        return arrows

    def init_props(self, prop_type: PropTypes) -> Dict[Colors, Prop]:
        red_prop_Dict = {
            COLOR: RED,
            PROP_TYPE: prop_type,
            LOCATION: None,
            LAYER: None,
            ORIENTATION: None,
        }
        blue_prop_Dict = {
            COLOR: BLUE,
            PROP_TYPE: prop_type,
            LOCATION: None,
            LAYER: None,
            ORIENTATION: None,
        }

        prop_class_mapping = {
            STAFF.lower(): Staff,
            BIGSTAFF.lower(): BigStaff,
            CLUB.lower(): Club,
            FAN.lower(): Fan,
            BIGFAN.lower(): BigFan,
            MINIHOOP.lower(): MiniHoop,
            BUUGENG.lower(): Buugeng,
            BIGBUUGENG.lower(): BigBuugeng,
            TRIAD.lower(): Triad,
            BIGTRIAD.lower(): BigTriad,
            DOUBLESTAR.lower(): DoubleStar,
            BIGHOOP.lower(): BigHoop,
            BIGDOUBLESTAR.lower(): BigDoubleStar,
            QUIAD.lower(): Quiad,
            SWORD.lower(): Sword,
            GUITAR.lower(): Guitar,
            UKULELE.lower(): Ukulele,
            CHICKEN.lower(): Chicken,
        }

        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")

        red_prop: Prop = prop_class(self.pictograph, red_prop_Dict, None)
        blue_prop: Prop = prop_class(self.pictograph, blue_prop_Dict, None)

        red_prop.set_svg_color(RED)
        blue_prop.set_svg_color(BLUE)

        props = {RED: red_prop, BLUE: blue_prop}
        for motion in self.pictograph.motions.values():
            for prop in props.values():
                if prop.color == motion.color:
                    motion.prop = prop
        return props

    def init_ghost_arrows(self) -> Dict[Colors, GhostArrow]:
        default_red_ghost_arrow_attributes = {
            COLOR: RED,
            MOTION_TYPE: STATIC,
            TURNS: 0,
        }

        default_blue_ghost_arrow_attributes = {
            COLOR: BLUE,
            MOTION_TYPE: STATIC,
            TURNS: 0,
        }

        red_ghost_arrow = GhostArrow(
            self.pictograph,
            default_red_ghost_arrow_attributes,
            None,
        )
        blue_ghost_arrow = GhostArrow(
            self.pictograph,
            default_blue_ghost_arrow_attributes,
            None,
        )

        ghost_arrows = {RED: red_ghost_arrow, BLUE: blue_ghost_arrow}
        for ghost_arrow in ghost_arrows.values():
            for arrow in self.pictograph.arrows.values():
                if arrow.color == ghost_arrow.color:
                    arrow.ghost = ghost_arrow
        return ghost_arrows

    def init_ghost_props(self, prop_type: PropTypes) -> Dict[Colors, GhostProp]:
        prop_class_mapping = {
            STAFF.lower(): Staff,
            BIGSTAFF.lower(): BigStaff,
            CLUB.lower(): Club,
            FAN.lower(): Fan,
            BIGFAN.lower(): BigFan,
            MINIHOOP.lower(): MiniHoop,
            BIGHOOP.lower(): BigHoop,
            BUUGENG.lower(): Buugeng,
            BIGBUUGENG.lower(): BigBuugeng,
            TRIAD.lower(): Triad,
            BIGTRIAD.lower(): BigTriad,
            DOUBLESTAR.lower(): DoubleStar,
            BIGDOUBLESTAR.lower(): BigDoubleStar,
            QUIAD.lower(): Quiad,
            SWORD.lower(): Sword,
            GUITAR.lower(): Guitar,
            UKULELE.lower(): Ukulele,
            CHICKEN.lower(): Chicken,
        }

        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")

        default_red_ghost_prop_attributes = {
            COLOR: RED,
            PROP_TYPE: prop_type,
            LOCATION: EAST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        default_blue_ghost_prop_attributes = {
            COLOR: BLUE,
            PROP_TYPE: prop_type,
            LOCATION: WEST,
            LAYER: 1,
            ORIENTATION: IN,
        }

        red_ghost_prop = GhostProp(
            self.pictograph,
            default_red_ghost_prop_attributes,
            self.pictograph.motions[RED],
        )
        blue_ghost_prop = GhostProp(
            self.pictograph,
            default_blue_ghost_prop_attributes,
            self.pictograph.motions[BLUE],
        )

        ghost_props = {RED: red_ghost_prop, BLUE: blue_ghost_prop}
        for ghost_prop in ghost_props.values():
            for prop in self.pictograph.props.values():
                if prop.color == ghost_prop.color:
                    prop.ghost = ghost_prop
        return ghost_props

    def init_letter_item(self) -> LetterItem:
        letter_item = LetterItem(self.pictograph)
        self.pictograph.addItem(letter_item)
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
