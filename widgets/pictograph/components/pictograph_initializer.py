from typing import TYPE_CHECKING
from PyQt6.QtCore import QPointF, QPoint, Qt
from Enums.MotionAttributes import Color, Location
from data.prop_class_mapping import prop_class_mapping
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from objects.prop.prop_classes import *

from constants import *
from widgets.factories.prop_factory import PropFactory
from widgets.pictograph.components.elemental_glyph.elemental_glyph import ElementalGlyph
from widgets.pictograph.components.tka_glyph.tka_glyph import TKA_Glyph

from widgets.pictograph.components.vtg_glyph.vtg_glyph import (
    VTG_Glyph,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographInitializer:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.pictograph.setSceneRect(0, 0, 950, 950)
        self.pictograph.setBackgroundBrush(Qt.GlobalColor.white)
        self.prop_factory = PropFactory()

    ### INIT ###

    def init_all_components(self) -> None:
        self.pictograph.dragged_prop = None
        self.pictograph.dragged_arrow = None

        self.pictograph.grid = self.init_grid()
        self.pictograph.locations = self.init_quadrant_boundaries(self.pictograph.grid)
        self.pictograph.motions = self.init_motions()
        self.pictograph.arrows = self.init_arrows()
        self.pictograph.props = self.init_props()
        self.pictograph.tka_glyph = self.init_tka_glyph()
        self.pictograph.vtg_glyph = self.init_vtg_glyph()
        self.pictograph.elemental_glyph = self.init_elemental_glyph()

    def init_grid(self) -> Grid:
        grid = Grid(self.pictograph)
        grid_position = QPointF(0, 0)
        grid.setPos(grid_position)
        self.pictograph.grid = grid
        return grid

    def init_motions(self) -> dict[Color, Motion]:
        motions: dict[Color, Motion] = {}
        for color in [Color.RED, Color.BLUE]:
            motions[color] = self._create_motion(color)
        self.pictograph.red_motion, self.pictograph.blue_motion = (
            motions[Color.RED],
            motions[Color.BLUE],
        )
        for motion in motions.values():
            motion.start_ori = None
            motion.end_ori = None
        return motions

    def init_arrows(self) -> dict[Color, Arrow]:
        arrows = {}
        for color in [Color.BLUE, Color.RED]:
            arrows[color] = self._create_arrow(color)
        self.pictograph.red_arrow, self.pictograph.blue_arrow = (
            arrows[Color.RED],
            arrows[Color.BLUE],
        )
        return arrows

    def init_props(self) -> dict[Color, Prop]:
        props: dict[Color, Prop] = {}
        prop_type = self.pictograph.main_widget.prop_type
        for color in [Color.RED, Color.BLUE]:
            initial_prop_attributes = {
                COLOR: color,
                PROP_TYPE: prop_type,
                LOC: None,
                ORI: None,
            }
            initial_prop_class = prop_class_mapping.get(prop_type)
            if initial_prop_class is None:
                raise ValueError(f"Invalid prop_type: {prop_type}")
            initial_prop = initial_prop_class(
                self.pictograph, initial_prop_attributes, None
            )
            props[color] = self.prop_factory.create_prop_of_type(
                initial_prop, prop_type
            )
            self.pictograph.motions[color].prop = props[color]
            props[color].motion = self.pictograph.motions[color]

            props[color].arrow = self.pictograph.motions[color].arrow
            self.pictograph.motions[color].arrow.motion.prop = props[color]
            self.pictograph.addItem(props[color])
            props[color].hide()

        self.pictograph.red_prop, self.pictograph.blue_prop = (
            props[Color.RED],
            props[Color.BLUE],
        )
        return props

    def init_tka_glyph(self) -> TKA_Glyph:
        tka_glyph = TKA_Glyph(self.pictograph)
        self.pictograph.addItem(tka_glyph)
        return tka_glyph

    def init_vtg_glyph(self) -> VTG_Glyph:
        vtg_glyph = VTG_Glyph(self.pictograph)
        return vtg_glyph

    def init_elemental_glyph(self) -> ElementalGlyph:
        elemental_glyph = ElementalGlyph(self.pictograph)
        return elemental_glyph

    def init_quadrant_boundaries(
        self, grid: Grid
    ) -> dict[Location, tuple[int, int, int, int]]:
        grid_center: QPoint = grid.grid_data.center_point.coordinates.toPoint()

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

    def _create_arrow(self, color: Color) -> Arrow:
        arrow_attributes = {
            COLOR: color,
            TURNS: 0,
        }
        arrow = Arrow(self.pictograph, arrow_attributes)
        self.pictograph.motions[color].arrow = arrow
        arrow.motion = self.pictograph.motions[color]
        self.pictograph.addItem(arrow)
        arrow.hide()
        return arrow

    def _create_motion(self, color: Color) -> Motion:
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
