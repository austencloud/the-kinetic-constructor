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
from objects.prop.prop_placement_manager.beta_prop_direction_calculator import (
    BetaPropDirectionCalculator,
)
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Directions
from utilities.TypeChecking.prop_types import (
    PropTypesList,
    big_bilateral_prop_types,
    big_unilateral_prop_types,
    small_bilateral_prop_types,
    small_unilateral_prop_types,
)

from utilities.TypeChecking.prop_types import (
    non_strictly_placed_props,
    strictly_placed_props,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PropPlacementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.letters: Dict[
            all_letters, List[Dict[str, str]]
        ] = pictograph.main_widget.letters
        self.position_offsets_cache = {}
        self.location_points_cache = {}
        self.direction_calculator = BetaPropDirectionCalculator(self)

    def update_prop_positions(self) -> None:
        self.red_motion = self.pictograph.motions[RED]
        self.blue_motion = self.pictograph.motions[BLUE]
        self.red_prop = self.pictograph.props[RED]
        self.blue_prop = self.pictograph.props[BLUE]

        self.motions = self.pictograph.motions.values()
        self.props = self.pictograph.props.values()
        self.ghost_props = self.pictograph.ghost_props.values()

        self.letter = self.pictograph.letter
        self.letter_type = self.pictograph.letter_type
        self.prop_type_counts = self._count_prop_types()

        for prop in self.props:
            self._set_prop_to_default_location(prop)
        for ghost_prop in self.ghost_props:
            self._set_prop_to_default_location(ghost_prop)

        if self.pictograph.has_props_in_beta():
            self._reposition_beta_props()

    def reposition_G_H(self) -> None:
        further_direction = self.direction_calculator.determine_translation_direction(
            self.red_motion
        )
        other_direction = self.direction_calculator.get_opposite_direction(
            further_direction
        )
        new_red_pos = self._calculate_new_position(
            self.red_prop.pos(), further_direction
        )
        new_blue_pos = self._calculate_new_position(
            self.blue_prop.pos(), other_direction
        )
        self.red_prop.setPos(new_red_pos)
        self.blue_prop.setPos(new_blue_pos)

    def reposition_I(self) -> None:
        pro_prop = (
            self.red_prop if self.red_motion.motion_type == PRO else self.blue_prop
        )
        anti_prop = (
            self.red_prop if self.red_motion.motion_type == ANTI else self.blue_prop
        )
        pro_motion = self.pictograph.motions[pro_prop.color]
        pro_direction = self._determine_translation_direction(pro_motion)
        anti_direction = self._get_opposite_direction(pro_direction)
        new_pro_position = self._calculate_new_position(pro_prop.pos(), pro_direction)
        new_anti_position = self._calculate_new_position(
            anti_prop.pos(), anti_direction
        )
        pro_prop.setPos(new_pro_position)
        anti_prop.setPos(new_anti_position)

    def reposition_J_K_L(self) -> None:
        red_direction = self.direction_calculator.determine_translation_direction(
            self.red_motion
        )
        blue_direction = self.direction_calculator.determine_translation_direction(
            self.blue_motion
        )

        if red_direction and blue_direction:
            self._move_prop(self.red_prop, red_direction)
            self._move_prop(self.blue_prop, blue_direction)

    def reposition_Y_Z(self) -> None:
        shift = self.red_motion if self.red_motion.is_shift() else self.blue_motion
        static_motion = (
            self.red_motion if self.red_motion.is_static() else self.blue_motion
        )

        direction = self._determine_translation_direction(shift)
        if direction:
            self._move_prop(
                next(prop for prop in self.props if prop.color == shift.color),
                direction,
            )
            self._move_prop(
                next(prop for prop in self.props if prop.color == static_motion.color),
                self._get_opposite_direction(direction),
            )

    def reposition_Y_dash_Z_dash(self) -> None:
        shift = self.red_motion if self.red_motion.is_shift() else self.blue_motion
        dash = self.red_motion if self.red_motion.is_dash() else self.blue_motion

        direction = self._determine_translation_direction(shift)
        if direction:
            self._move_prop(
                next(prop for prop in self.props if prop.color == shift.color),
                direction,
            )
            self._move_prop(
                next(prop for prop in self.props if prop.color == dash.color),
                self._get_opposite_direction(direction),
            )

    def reposition_Ψ(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.direction_calculator._get_translation_dir_for_non_shift(
                self.red_prop
            )
            if direction:
                self._move_prop(self.red_prop, direction)
                self._move_prop(
                    self.blue_prop,
                    self.direction_calculator.get_opposite_direction(direction),
                )

        elif self.red_prop.prop_type in strictly_placed_props:
            self._set_prop_to_default_location(self.red_prop)

    def reposition_Ψ_dash(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.direction_calculator._get_translation_dir_for_non_shift(
                self.red_prop
            )
            if direction:
                self._move_prop(self.red_prop, direction)
                self._move_prop(self.blue_prop, self._get_opposite_direction(direction))

        elif self.red_prop.prop_type in strictly_placed_props:
            self._set_prop_to_default_location()(self.red_prop)

    def reposition_β(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.direction_calculator._get_translation_dir_for_non_shift(
                self.red_prop
            )
            if direction:
                self._move_prop(self.red_prop, direction)
                self._move_prop(self.blue_prop, self._get_opposite_direction(direction))

        elif self.red_prop.prop_type in strictly_placed_props:
            self._set_prop_to_default_location()(self.red_prop)

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

    def _reposition_small_bilateral_props(self) -> None:
        if self.pictograph.has_hybrid_orientations():
            for prop in self.props:
                self._set_prop_to_default_location(prop)

        else:
            if self.letter in ["G", "H"]:
                self.reposition_G_H()
            elif self.letter == "I":
                self.reposition_I()
            elif self.letter in ["J", "K", "L"]:
                self.reposition_J_K_L()
            elif self.letter in ["Y", "Z"]:
                self.reposition_Y_Z()
            elif self.letter == "β":
                self.reposition_β()
            elif self.letter in ["Y-", "Z-"]:
                self.reposition_Y_dash_Z_dash()
            elif self.letter == "Ψ":
                self.reposition_Ψ()
            elif self.letter == "Ψ-":
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
                ) = self.direction_calculator.determine_direction_for_unilateral_props(
                    self.red_motion
                )
                self._move_prop(self.red_prop, red_direction)
                self._move_prop(self.blue_prop, blue_direction)
        else:
            for prop in small_unilateral_props:
                self._set_prop_to_default_location(prop)

    def _reposition_big_props(
        self, big_unilateral_props: List[Prop], big_bilateral_props: List[Prop]
    ) -> None:
        big_props = big_unilateral_props + big_bilateral_props
        if self.pictograph.has_non_hybrid_orientations():
            for prop in big_props:
                self._set_prop_to_default_location(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self.direction_calculator.determine_direction_for_unilateral_props(
                    self.red_motion
                )
                self._move_prop(self.red_prop, red_direction)
                self._move_prop(self.blue_prop, blue_direction)
        else:
            for prop in big_props:
                self._set_prop_to_default_location(prop)

    ### HELPERS ###

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
