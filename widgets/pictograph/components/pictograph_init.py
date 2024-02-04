from typing import TYPE_CHECKING
from PyQt6.QtCore import QPointF, QPoint, Qt

from objects.arrow.arrow import Arrow
from objects.arrow.ghost_arrow import GhostArrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.ghost_prop import GhostProp
from objects.prop.prop import Prop
from objects.prop.prop_classes import *

from utilities.TypeChecking.prop_types import PropTypes
from utilities.letter_item import LetterItem
from utilities.TypeChecking.MotionAttributes import Colors, Locations, MotionTypes
from constants import *
from widgets.factories.prop_factory import PropFactory

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographInit:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph
        self.p.setSceneRect(0, 0, 950, 950)
        self.p.setBackgroundBrush(Qt.GlobalColor.white)
        self.prop_factory = PropFactory()

    ### INIT ###

    def init_all_components(self) -> None:
        self.p.dragged_prop = None
        self.p.dragged_arrow = None

        self.p.grid = self.init_grid()
        self.p.locations = self.init_quadrant_boundaries(self.p.grid)

        self.p.motions = self.init_motions()
        self.p.arrows = self.init_arrows()
        self.p.props = self.init_props()
        self.p.letter_item = self.init_letter_item()

    def init_grid(self) -> Grid:
        grid = Grid(self.p)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)

        self.p.grid = grid
        return grid

    def init_motions(self) -> dict[Colors, Motion]:
        motions = {}
        for color in [RED, BLUE]:
            motions[color] = self._create_motion(color)
        self.p.red_motion, self.p.blue_motion = (motions[RED], motions[BLUE])
        return motions

    def init_arrows(self) -> dict[Colors, Arrow]:
        arrows = {}
        for color in [BLUE, RED]:
            arrows[color] = self._create_arrow(color)
        self.p.red_arrow, self.p.blue_arrow = (arrows[RED], arrows[BLUE])
        return arrows

    def init_props(self) -> dict[Colors, Prop]:
        props: dict[Colors, Prop] = {}
        prop_type = self.p.main_widget.prop_type
        for color in [RED, BLUE]:
            initial_prop_attributes = {
                COLOR: color,
                PROP_TYPE: prop_type,
                LOC: None,
                ORI: None,
            }
            initial_prop_class = prop_class_mapping.get(prop_type.lower())
            if initial_prop_class is None:
                raise ValueError(f"Invalid prop_type: {prop_type}")
            initial_prop = initial_prop_class(self.p, initial_prop_attributes, None)
            props[color] = self.prop_factory.create_prop_of_type(
                initial_prop, prop_type
            )
            self.p.motions[color].prop = props[color]
            props[color].motion = self.p.motions[color]

            props[color].arrow = self.p.motions[color].arrow
            self.p.motions[color].arrow.motion.prop = props[color]
            self.p.addItem(props[color])
            props[color].hide()

        self.p.red_prop, self.p.blue_prop = (props[RED], props[BLUE])
        return props

    def init_letter_item(self) -> LetterItem:
        letter_item = LetterItem(self.p)
        self.p.addItem(letter_item)
        return letter_item

    def init_quadrant_boundaries(
        self, grid: Grid
    ) -> dict[Locations, tuple[int, int, int, int]]:
        grid_center: QPoint = grid.grid_data.center_point.coordinates.toPoint()

        grid_center_x = grid_center.x()
        grid_center_y = grid_center.y()

        ne_boundary = (
            grid_center_x,
            0,
            self.p.width(),
            grid_center_y,
        )
        se_boundary = (
            grid_center_x,
            grid_center_y,
            self.p.width(),
            self.p.height(),
        )
        sw_boundary = (0, grid_center_y, grid_center_x, self.p.height())
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

    def _create_arrow(self, color: Colors) -> Arrow:
        arrow_attributes = {
            COLOR: color,
            TURNS: 0,
        }
        arrow = Arrow(self.p, arrow_attributes)
        self.p.motions[color].arrow = arrow
        arrow.motion = self.p.motions[color]
        self.p.addItem(arrow)
        arrow.hide()
        return arrow

    def _create_prop(self, color: Colors, prop_type: PropTypes) -> Prop:
        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")
        prop_attributes = {
            COLOR: color,
            PROP_TYPE: prop_type,
            LOC: None,
            ORI: None,
        }
        prop: Prop = prop_class(self.p, prop_attributes, None)
        self.p.motions[color].prop = prop
        prop.motion = self.p.motions[color]
        self.p.addItem(prop)
        prop.hide()
        return prop

    def _create_motion(self, color: Colors) -> Motion:
        motion_dict = {
            COLOR: color,
            ARROW: None,
            PROP: None,
            MOTION_TYPE: None,
            PROP_ROT_DIR: None,
            TURNS: 0,
            START_LOC: None,
            END_LOC: None,
            START_ORI: None,
        }
        return Motion(self.p, motion_dict)


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
