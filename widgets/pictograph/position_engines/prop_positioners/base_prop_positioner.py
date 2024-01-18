from PyQt6.QtCore import QPointF


from typing import TYPE_CHECKING, Dict, List, Tuple, Union
from constants import (
    ANTIRADIAL,
    CLOCK,
    COUNTER,
    EAST,
    IN,
    NORTH,
    OUT,
    RADIAL,
    SOUTH,
    WEST,
    BLUE,
    RED,
    DIAMOND,
    BOX,
    PRO,
    ANTI,
    STATIC,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)

from objects.motion.motion import Motion
from objects.prop.prop import Prop
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Directions
from utilities.TypeChecking.prop_types import (
    PropTypesList,
    big_bilateral_prop_types,
    big_unilateral_prop_types,
    small_bilateral_prop_types,
    small_unilateral_prop_types,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from .by_letter_type.Type1_prop_positioner import Type1PropPositioner
    from .by_letter_type.Type2_prop_positioner import Type2PropPositioner
    from .by_letter_type.Type3_prop_positioner import Type3PropPositioner
    from .by_letter_type.Type4_prop_positioner import Type4PropPositioner
    from .by_letter_type.Type5_prop_positioner import Type5PropPositioner
    from .by_letter_type.Type6_prop_positioner import Type6PropPositioner


class BasePropPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.letters: Dict[
            all_letters, List[Dict[str, str]]
        ] = pictograph.main_widget.letters
        self.position_offsets_cache = {}
        self.location_points_cache = {}

    def update_prop_positions(self) -> None:
        self.red_motion = self.pictograph.motions[RED]
        self.blue_motion = self.pictograph.motions[BLUE]
        self.red_prop = self.pictograph.props[RED]
        self.blue_prop = self.pictograph.props[BLUE]

        self.motions = self.pictograph.motions.values()
        self.props = self.pictograph.props.values()
        self.ghost_props = self.pictograph.ghost_props.values()

        self.current_letter = self.pictograph.letter
        self.prop_type_counts = self._count_prop_types()

        for prop in self.props:
            self._set_prop_to_default_location(prop)
        for ghost_prop in self.ghost_props:
            self._set_prop_to_default_location(ghost_prop)

        if self.pictograph.has_props_in_beta():
            self._reposition_beta_props()

    def _count_prop_types(self) -> Dict[str, int]:
        return {
            ptype: sum(prop.prop_type == ptype for prop in self.props)
            for ptype in PropTypesList
        }

    def _set_prop_to_default_location(self, prop: Prop, strict: bool = False) -> None:
        if prop in self.position_offsets_cache:
            position_offsets = self.position_offsets_cache[prop]
        else:
            position_offsets = self._get_position_offsets(prop)
        key = (prop.ori, prop.loc)
        offset = position_offsets.get(key, QPointF(0, 0))
        prop.setTransformOriginPoint(0, 0)

        if self.pictograph.grid.grid_mode == DIAMOND:
            location_points = self._get_location_points(strict, DIAMOND)
        elif self.pictograph.grid.grid_mode == BOX:
            location_points = self._get_location_points(strict, BOX)

        for location, location_point in location_points.items():
            if prop.loc == location[0]:
                prop.setPos(location_point + offset)
                return

    def _get_location_points(self, strict: bool, grid_mode: str) -> Dict[str, QPointF]:
        strict_key = "strict" if strict else "normal"
        location_points = self.pictograph.grid.circle_coordinates_cache["hand_points"][
            grid_mode
        ][strict_key]
        return location_points

    def _reposition_small_bilateral_props(
        self: Union[
            "Type1PropPositioner",
            "Type2PropPositioner",
            "Type3PropPositioner",
            "Type4PropPositioner",
            "Type5PropPositioner",
            "Type6PropPositioner",
        ]
    ) -> None:
        if self.pictograph.has_hybrid_orientations():
            for prop in self.props:
                self._set_prop_to_default_location(prop)

        else:
            if self.current_letter in ["G", "H"]:
                self.reposition_G_H()
            elif self.current_letter == "I":
                self.reposition_I()
            elif self.current_letter in ["J", "K", "L"]:
                self.reposition_J_K_L()
            elif self.current_letter in ["Y", "Z"]:
                self.reposition_Y_Z()
            elif self.current_letter == "β":
                self.reposition_β()
            elif self.current_letter in ["Y-", "Z-"]:
                self.reposition_Y_dash_Z_dash()
            elif self.current_letter == "Ψ":
                self.reposition_Ψ()
            elif self.current_letter == "Ψ-":
                self.reposition_Ψ_dash()

    def _move_prop(self, prop: Prop, direction: Directions) -> None:
        new_position = self._calculate_new_position(prop.pos(), direction)
        prop.setPos(new_position)

    ### REPOSITIONING ###

    def _reposition_beta_props(self) -> None:
        big_unilateral_props: List[Prop] = [
            prop for prop in self.props if prop.prop_type in big_unilateral_prop_types
        ]
        small_unilateral_props: List[Prop] = [
            prop for prop in self.props if prop.prop_type in small_unilateral_prop_types
        ]
        small_bilateral_props: List[Prop] = [
            prop for prop in self.props if prop.prop_type in small_bilateral_prop_types
        ]
        big_bilateral_props: List[Prop] = [
            prop for prop in self.props if prop.prop_type in big_bilateral_prop_types
        ]
        big_props = big_unilateral_props + big_bilateral_props
        small_props = small_unilateral_props + small_bilateral_props
        if len(big_props) == 2:
            self._reposition_big_props(big_unilateral_props, big_bilateral_props)
        elif len(small_props) == 2:
            self._reposition_small_props(small_unilateral_props, small_bilateral_props)

    def _reposition_small_props(self, small_unilateral_props, small_bilateral_props):
        if len(small_unilateral_props) == 2:
            self._reposition_small_unilateral_props(small_unilateral_props)
        elif len(small_bilateral_props) == 2:
            self._reposition_small_bilateral_props()

    def _reposition_small_unilateral_props(self, small_unilateral_props: List[Prop]):
        if small_unilateral_props[0].ori == small_unilateral_props[1].ori:
            for prop in small_unilateral_props:
                self._set_prop_to_default_location(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self._determine_translation_direction_for_unilateral_props(
                    self.red_motion, self.blue_motion
                )
                self._move_prop(self.red_prop, red_direction)
                self._move_prop(self.blue_prop, blue_direction)
        else:
            for prop in small_unilateral_props:
                self._set_prop_to_default_location(prop)

    def _reposition_big_props(
        self, big_unilateral_props: List[Prop], big_bilateral_props: List[Prop]
    ):
        big_props = big_unilateral_props + big_bilateral_props
        if self.pictograph.has_non_hybrid_orientations():
            for prop in big_props:
                self._set_prop_to_default_location(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self._determine_translation_direction_for_unilateral_props(
                    self.red_motion, self.blue_motion
                )
                self._move_prop(self.red_prop, red_direction)
                self._move_prop(self.blue_prop, blue_direction)
        else:
            for prop in big_props:
                self._set_prop_to_default_location(prop)

    def _determine_translation_direction_for_unilateral_props(
        self, red_motion: Motion, blue_motion: Motion
    ) -> Tuple[Directions]:
        """Determine the translation direction for big unilateral props based on the motion type, start location, end location."""
        red_direction = self._get_direction_for_motion(red_motion)
        blue_direction = self._get_opposite_direction(red_direction)

        # Ensure that both directions are set, defaulting to None if necessary
        return (red_direction or None, blue_direction or None)

    def _get_direction_for_motion(self, motion: Motion) -> Directions | None:
        """Determine the direction based on a single motion."""
        if motion.end_ori in [
            IN,
            OUT,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_loc in [NORTH, SOUTH]:
                return RIGHT if motion.start_loc == EAST else LEFT
            elif motion.end_loc in [EAST, WEST]:
                return DOWN if motion.start_loc == SOUTH else UP
        elif motion.end_ori in [
            CLOCK,
            COUNTER,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_loc in [NORTH, SOUTH]:
                return UP if motion.start_loc == EAST else DOWN
            elif motion.end_loc in [EAST, WEST]:
                return RIGHT if motion.start_loc == SOUTH else LEFT
        return None

    def _get_translation_dir_for_non_shift(
        self, prop: Prop, end_loc: str
    ) -> Directions | None:
        layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP if end_loc == EAST else None,
                (WEST, BLUE): DOWN if end_loc == WEST else None,
                (WEST, RED): UP if end_loc == WEST else None,
                (EAST, BLUE): DOWN if end_loc == EAST else None,
            },
            ANTIRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT if end_loc == EAST else None,
                (WEST, BLUE): LEFT if end_loc == WEST else None,
                (WEST, RED): RIGHT if end_loc == WEST else None,
                (EAST, BLUE): LEFT if end_loc == EAST else None,
            },
        }
        if prop.is_radial():
            return layer_reposition_map[RADIAL][(prop.loc, prop.color)]
        elif prop.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.loc, prop.color)]

    ### HELPERS ###

    def _determine_translation_direction(self, motion: Motion) -> Directions:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if not (motion.is_shift() or motion.is_static()):
            return None

        if motion.prop.is_radial():
            return self._get_translation_dir_for_radial(motion)
        elif motion.prop.is_antiradial():
            return self._get_translation_dir_for_antiradial(motion)

    def _get_translation_dir_for_radial(self, motion: Motion) -> Directions | None:
        direction_map = {
            (NORTH, EAST): RIGHT,
            (NORTH, WEST): LEFT,
            (SOUTH, EAST): RIGHT,
            (SOUTH, WEST): LEFT,
            (EAST, NORTH): UP,
            (EAST, SOUTH): DOWN,
            (WEST, NORTH): UP,
            (WEST, SOUTH): DOWN,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def _get_translation_dir_for_antiradial(self, motion: Motion) -> Directions | None:
        direction_map = {
            (NORTH, EAST): UP,
            (NORTH, WEST): DOWN,
            (SOUTH, EAST): UP,
            (SOUTH, WEST): DOWN,
            (EAST, NORTH): RIGHT,
            (EAST, SOUTH): LEFT,
            (WEST, NORTH): RIGHT,
            (WEST, SOUTH): LEFT,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def _calculate_new_position(
        self,
        current_position: QPointF,
        direction: Directions,
    ) -> QPointF:
        self.beta_offset = self.pictograph.width() / 38

        offset_map = {
            LEFT: QPointF(-self.beta_offset, 0),
            RIGHT: QPointF(self.beta_offset, 0),
            UP: QPointF(0, -self.beta_offset),
            DOWN: QPointF(0, self.beta_offset),
        }
        offset = offset_map.get(direction, QPointF(0, 0))
        return current_position + offset

    ### GETTERS

    def _get_position_offsets(self, prop: Prop) -> Dict[Tuple[str, str], QPointF]:
        if prop in self.position_offsets_cache:
            return self.position_offsets_cache[prop]
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()

        x = prop_width / 2
        y = prop_length / 2

        # Define a map for position offsets based on orientation and location
        position_offsets = {
            (IN, NORTH): QPointF(x, -y),
            (IN, SOUTH): QPointF(-x, y),
            (IN, EAST): QPointF(y, x),
            (IN, WEST): QPointF(-y, -x),
            (OUT, NORTH): QPointF(-x, y),
            (OUT, SOUTH): QPointF(x, -y),
            (OUT, EAST): QPointF(-y, -x),
            (OUT, WEST): QPointF(y, x),
            (CLOCK, NORTH): QPointF(-y, -x),
            (CLOCK, SOUTH): QPointF(y, x),
            (CLOCK, EAST): QPointF(x, -y),
            (CLOCK, WEST): QPointF(-x, y),
            (COUNTER, NORTH): QPointF(y, x),
            (COUNTER, SOUTH): QPointF(-y, -x),
            (COUNTER, EAST): QPointF(-x, y),
            (COUNTER, WEST): QPointF(x, -y),
        }
        self.position_offsets_cache[prop] = position_offsets
        return position_offsets

    def _get_opposite_direction(self, movement: Directions) -> Directions:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
        }
        return opposite_directions.get(movement)

    def _get_translation_dir_for_non_shift(self, prop: Prop) -> Directions | None:
        layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
                (EAST, BLUE): DOWN,
            },
            ANTIRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT,
                (WEST, BLUE): LEFT,
                (WEST, RED): RIGHT,
                (EAST, BLUE): LEFT,
            },
        }
        if prop.is_radial():
            return layer_reposition_map[RADIAL][(prop.loc, prop.color)]
        elif prop.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.loc, prop.color)]
