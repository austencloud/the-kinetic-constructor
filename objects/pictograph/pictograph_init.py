from typing import TYPE_CHECKING, Dict, Tuple
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QGraphicsView
from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
    ArrowPlacementManager,
)
from objects.pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)

from objects.pictograph.pictograph_event_handler import PictographMouseEventHandler
from objects.pictograph.pictograph_image_renderer import PictographImageRenderer
from objects.pictograph.pictograph_state_updater import PictographStateUpdater
from objects.pictograph.position_engines.prop_positioners.main_prop_positioner import (
    PropPlacementManager,
)
from utilities.letter_engine import LetterEngine
from ..grid import Grid
from ..arrow.arrow import Arrow
from ..arrow.ghost_arrow import GhostArrow
from ..prop.ghost_prop import GhostProp
from ..prop.prop_types import *
from ..prop.prop import Prop
from ..motion.motion import Motion
from utilities.TypeChecking.prop_types import PropTypes
from utilities.letter_item import LetterItem
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
)
from constants import *

if TYPE_CHECKING:
    from ..pictograph.pictograph import Pictograph


class PictographInit:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    ### INIT ###

    def init_all_components(self) -> None:
        self.pictograph.dragged_prop = None
        self.pictograph.dragged_arrow = None

        self.pictograph.grid: Grid = self.init_grid()
        self.pictograph.locations: Dict[
            Locations, Tuple[int, int, int, int]
        ] = self.init_quadrant_boundaries(self.pictograph.grid)

        self.pictograph.motions: Dict[Colors, Motion] = self.init_motions()
        self.pictograph.red_motion, self.pictograph.blue_motion = (
            self.pictograph.motions[RED],
            self.pictograph.motions[BLUE],
        )
        self.pictograph.arrows, self.pictograph.ghost_arrows = self.init_arrows()
        self.pictograph.red_arrow, self.pictograph.blue_arrow = (
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        )
        self.pictograph.props, self.pictograph.ghost_props = self.init_props(
            self.pictograph.main_widget.prop_type
        )
        self.pictograph.red_prop, self.pictograph.blue_prop = (
            self.pictograph.props[RED],
            self.pictograph.props[BLUE],
        )

        self.pictograph.view = self.init_view(self.pictograph.graph_type)
        self.pictograph.letter_item: LetterItem = self.init_letter_item()

    def init_view(self, graph_type) -> QGraphicsView:
        from widgets.graph_editor_tab.graph_editor_pictograph_view import (
            GraphEditorPictographView,
        )
        from widgets.option_picker_tab.option import OptionView
        from widgets.sequence_widget.beat_frame.start_pos_beat import (
            StartPositionBeatView,
        )
        from widgets.sequence_widget.beat_frame.beat import BeatView
        from widgets.ig_tab.ig_pictograph import IGPictographView

        if graph_type == MAIN:
            view = GraphEditorPictographView(self.pictograph)
        elif graph_type == OPTION:
            view = OptionView(self.pictograph)
        elif graph_type == BEAT:
            view = BeatView(self.pictograph)
        elif graph_type == START_POS_BEAT:
            view = StartPositionBeatView(self.pictograph)
        elif graph_type == IG_PICTOGRAPH:
            view = IGPictographView(self.pictograph)
        return view

    def init_grid(self) -> Grid:
        grid = Grid(self.pictograph)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)

        self.pictograph.grid = grid
        return grid

    def init_motions(self) -> Dict[Colors, Motion]:
        return {color: self._create_motion(color) for color in [RED, BLUE]}

    def init_objects(self, prop_type: PropTypes) -> None:
        self.init_grid()
        self.pictograph.motions = self.init_motions()
        self.pictograph.arrows, self.pictograph.ghost_arrows = self.init_arrows()
        self.pictograph.props, self.pictograph.ghost_props = self.init_props(prop_type)

    def init_arrows(self) -> Tuple[Dict[Colors, Arrow], Dict[Colors, GhostArrow]]:
        arrows = {}
        ghost_arrows = {}
        for color in [BLUE, RED]:
            arrows[color], ghost_arrows[color] = self._create_arrow(color, None)
        return arrows, ghost_arrows

    def init_props(
        self, prop_type: PropTypes
    ) -> Tuple[Dict[Colors, Prop], Dict[Colors, GhostProp]]:
        props = {}
        ghost_props = {}
        for color in [RED, BLUE]:
            props[color], ghost_props[color] = self._create_prop(color, prop_type)
        return props, ghost_props

    def init_letter_item(self) -> LetterItem:
        letter_item = LetterItem(self.pictograph)
        self.pictograph.addItem(letter_item)
        return letter_item

    def init_quadrant_boundaries(
        self, grid: Grid
    ) -> Dict[Locations, Tuple[int, int, int, int]]:
        # Use cached coordinates directly
        grid_center = grid.circle_coordinates_cache["center_point"].toPoint()

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

    def _create_arrow(
        self, color: Colors, motion_type: MotionTypes
    ) -> Tuple[Arrow, GhostArrow]:
        arrow_attributes = {
            COLOR: color,
            TURNS: 0,
        }
        arrow = Arrow(self.pictograph, arrow_attributes, self.pictograph.motions[color])
        ghost_arrow = GhostArrow(
            self.pictograph, arrow_attributes, self.pictograph.motions[color]
        )
        arrow.ghost = ghost_arrow
        self.pictograph.motions[color].arrow = arrow
        arrow.motion = self.pictograph.motions[color]
        ghost_arrow.motion = self.pictograph.motions[color]
        arrow.ghost = ghost_arrow
        self.pictograph.addItem(arrow)
        arrow.hide()
        return arrow, ghost_arrow

    def _create_prop(
        self, color: Colors, prop_type: PropTypes
    ) -> Tuple[Prop, GhostProp]:
        prop_class = prop_class_mapping.get(prop_type)
        if prop_class is None:
            raise ValueError(f"Invalid prop_type: {prop_type}")
        prop_attributes = {
            COLOR: color,
            PROP_TYPE: prop_type,
            LOC: None,
            ORI: None,
        }
        prop: Prop = prop_class(self.pictograph, prop_attributes, None)
        ghost_prop = GhostProp(
            self.pictograph, prop_attributes, self.pictograph.motions[color]
        )
        self.pictograph.motions[color].prop = prop
        prop.motion = self.pictograph.motions[color]
        ghost_prop.motion = self.pictograph.motions[color]
        prop.ghost = ghost_prop
        prop.arrow = self.pictograph.motions[color].arrow
        self.pictograph.motions[color].arrow.prop = prop
        self.pictograph.addItem(prop)
        prop.hide()
        return prop, ghost_prop

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
        return Motion(self.pictograph, motion_dict)


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
