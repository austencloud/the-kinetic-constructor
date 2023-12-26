from PyQt6.QtCore import QPointF

import pandas as pd
from Enums import *

from typing import TYPE_CHECKING, Dict, List, Tuple
from constants import (
    CLOCK,
    COUNTER,
    EAST,
    IN,
    NORTH,
    OUT,
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

from objects.motion import Motion
from objects.prop.prop import Prop


BETA_OFFSET = 25

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class PropPositioner:
    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.letters: pd.DataFrame = scene.main_widget.letters

    def update_prop_positions(self) -> None:
        self.prop_type_counts = self._count_prop_types()
        for prop in self.scene.props.values():
            if any(
                self.prop_type_counts[prop_type] == 2
                for prop_type in strictly_placed_props
            ):
                self._set_strict_prop_location(prop)
            else:
                self._set_default_prop_location(prop)

        for prop in self.scene.ghost_props.values():
            if any(
                self.prop_type_counts[ptype] == 2 for ptype in strictly_placed_props
            ):
                self._set_strict_prop_location(prop)
            else:
                self._set_default_prop_location(prop)

        if self._props_in_beta():
            self._reposition_beta_props()

    def _count_prop_types(self) -> Dict[str, int]:
        return {
            ptype.value: sum(
                prop.prop_type == ptype for prop in self.scene.props.values()
            )
            for ptype in PropType
        }

    def _set_strict_prop_location(self, prop: "Prop") -> None:
        position_offsets = self._get_position_offsets(prop)
        key = (prop.orientation, prop.location)
        offset = position_offsets.get(key, QPointF(0, 0))
        prop.setTransformOriginPoint(0, 0)
        if self.scene.grid.grid_mode == DIAMOND:
            if prop.location in self.scene.grid.strict_diamond_hand_points:
                prop.setPos(
                    self.scene.grid.strict_diamond_hand_points[prop.location] + offset
                )

    def _set_default_prop_location(self, prop: "Prop") -> None:
        position_offsets = self._get_position_offsets(prop)
        key = (prop.orientation, prop.location)
        offset = position_offsets.get(key, QPointF(0, 0))
        prop.setTransformOriginPoint(0, 0)
        if self.scene.grid.grid_mode == DIAMOND:
            if prop.location in self.scene.grid.diamond_hand_points:
                prop.setPos(self.scene.grid.diamond_hand_points[prop.location] + offset)
        elif self.scene.grid.grid_mode == BOX:
            if prop.location in self.scene.grid.box_hand_points:
                prop.setPos(self.scene.grid.box_hand_points[prop.location] + offset)

    def _move_prop(self, prop: Prop, direction: Direction) -> None:
        new_position = self._calculate_new_position(prop.pos(), direction)
        prop.setPos(new_position)

    ### REPOSITIONING ###

    def _reposition_beta_props(self) -> None:
        state = self.scene.get_state()
        # Handle special case for certain props

        self.red_prop = self.scene.props[RED]
        self.blue_prop = self.scene.props[BLUE]

        big_unilateral_props: List[Prop] = [
            prop
            for prop in self.scene.props.values()
            if prop.prop_type in big_unilateral_prop_types
        ]

        small_unilateral_props: List[Prop] = [
            prop
            for prop in self.scene.props.values()
            if prop.prop_type in small_unilateral_prop_types
        ]

        small_bilateral_props: List[Prop] = [
            prop
            for prop in self.scene.props.values()
            if prop.prop_type in small_bilateral_prop_types
        ]

        big_bilateral_props: List[Prop] = [
            prop
            for prop in self.scene.props.values()
            if prop.prop_type in big_bilateral_prop_types
        ]
        if len(big_unilateral_props) == 2:
            self._reposition_big_unilateral_props(big_unilateral_props)
        elif len(small_unilateral_props) == 2:
            self._reposition_small_unilateral_props(small_unilateral_props)
        elif len(small_bilateral_props) == 2:
            pro_or_anti_motions = [
                color
                for color in [RED, BLUE]
                if state[f"{color}_motion_type"] in [PRO, ANTI]
            ]
            static_motions = [
                color
                for color in [RED, BLUE]
                if state[f"{color}_motion_type"] == STATIC
            ]

            # STATIC BETA - β
            if len(static_motions) > 1:
                self._reposition_static_beta()

            # BETA to BETA - G, H, I
            both = [
                color
                for color in [RED, BLUE]
                if state[f"{color}_motion_type"] in [PRO, ANTI]
            ]
            if (
                state["red_start_location"] == state["blue_start_location"]
                and state["red_end_location"] == state["blue_end_location"]
            ):
                if (
                    len(both) == 2
                    and len(set(state[color + "_motion_type"] for color in both)) == 1
                ):
                    self._reposition_G_and_H(state)
                elif (
                    self.scene.motions[RED].motion_type == PRO
                    and self.scene.motions[BLUE].motion_type == ANTI
                    or self.scene.motions[RED].motion_type == ANTI
                    and self.scene.motions[BLUE].motion_type == PRO
                ):
                    self._reposition_I(state)

            # GAMMA → BETA - Y, Z
            if len(pro_or_anti_motions) == 1 and len(static_motions) == 1:
                self.reposition_gamma_to_beta()

            # ALPHA → BETA - D, E, F
            if all(state[f"{color}_motion_type"] != STATIC for color in [RED, BLUE]):
                if state["red_start_location"] != state["blue_start_location"]:
                    self._reposition_alpha_to_beta(state)

    def _reposition_small_unilateral_props(self, small_unilateral_props: List[Prop]):
        if (
            small_unilateral_props[0].orientation
            == small_unilateral_props[1].orientation
        ):
            for prop in small_unilateral_props:
                self._set_default_prop_location(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self._determine_translation_direction_for_unilateral_props(
                    self.scene.motions[RED], self.scene.motions[BLUE]
                )
                if prop.color == RED:
                    self._move_prop(prop, red_direction)
                elif prop.color == BLUE:
                    self._move_prop(prop, blue_direction)
        else:
            for prop in small_unilateral_props:
                self._set_default_prop_location(prop)

    def _reposition_big_unilateral_props(self, big_unilateral_props: List[Prop]):
        if big_unilateral_props[0].orientation == big_unilateral_props[1].orientation:
            for prop in big_unilateral_props:
                self._set_strict_prop_location(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self._determine_translation_direction_for_unilateral_props(
                    self.scene.motions[RED], self.scene.motions[BLUE]
                )
                if prop.color == RED:
                    self._move_prop(prop, red_direction)
                elif prop.color == BLUE:
                    self._move_prop(prop, blue_direction)
        else:
            for prop in big_unilateral_props:
                self._set_strict_prop_location(prop)

    def _determine_translation_direction_for_unilateral_props(
        self, red_motion: Motion, blue_motion: Motion
    ) -> Tuple[Direction, Direction]:
        """Determine the translation direction for big unilateral props based on the motion type, start location, end location."""
        red_direction = self._get_direction_for_motion(red_motion)
        blue_direction = self._get_opposite_direction(red_direction)

        # Ensure that both directions are set, defaulting to None if necessary
        return (red_direction or None, blue_direction or None)

    def _get_direction_for_motion(self, motion: Motion) -> Direction | None:
        """Determine the direction based on a single motion."""
        if motion.end_orientation in [
            IN,
            OUT,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_location in [NORTH, SOUTH]:
                return RIGHT if motion.start_location == EAST else LEFT
            elif motion.end_location in [EAST, WEST]:
                return DOWN if motion.start_location == SOUTH else UP
        elif motion.end_orientation in [
            CLOCK,
            COUNTER,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_location in [NORTH, SOUTH]:
                return UP if motion.start_location == EAST else DOWN
            elif motion.end_location in [EAST, WEST]:
                return RIGHT if motion.start_location == SOUTH else LEFT
        return None

    ### STATIC BETA ### β
    def _reposition_static_beta(self) -> None:
        moved_props = set()  # To keep track of props that have already been moved

        for color, motion in self.scene.motions.items():
            prop = next(
                (p for p in self.scene.props.values() if p.color == color), None
            )
            if not prop or prop in moved_props:
                continue

            other_prop = next(
                (
                    other
                    for other in self.scene.props.values()
                    if other != prop and other.location == prop.location
                ),
                None,
            )

            if other_prop and (
                (other_prop.is_radial() and prop.is_radial())
                or (other_prop.is_antiradial() and prop.is_antiradial())
            ):
                if prop.prop_type in non_strictly_placed_props:
                    direction = self._determine_direction_for_static_beta(
                        prop, motion.end_location
                    )
                    if direction:
                        self._move_prop(prop, direction)
                        moved_props.add(prop)  # Mark this prop as moved
                elif prop.prop_type in strictly_placed_props:
                    self._set_strict_prop_location(other_prop)

    def _determine_direction_for_static_beta(
        self, prop: Prop, end_location: str
    ) -> Direction | None:
        layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP if end_location == EAST else None,
                (WEST, BLUE): DOWN if end_location == WEST else None,
                (WEST, RED): UP if end_location == WEST else None,
                (EAST, BLUE): DOWN if end_location == EAST else None,
            },
            ANTIRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT if end_location == EAST else None,
                (WEST, BLUE): LEFT if end_location == WEST else None,
                (WEST, RED): RIGHT if end_location == WEST else None,
                (EAST, BLUE): LEFT if end_location == EAST else None,
            },
        }
        if prop.is_radial():
            return layer_reposition_map[RADIAL][(prop.location, prop.color)]
        elif prop.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.location, prop.color)]

    ### ALPHA TO BETA ### J, K, L

    def _reposition_alpha_to_beta(self, state) -> None:
        # Extract motion type and end locations for both colors from the DataFrame row
        red_end_location = state["red_end_location"]
        blue_end_location = state["blue_end_location"]
        if (
            state["red_end_orientation"] in [CLOCK, COUNTER]
            and state["blue_end_orientation"] in [IN, OUT]
            or state["blue_end_orientation"]
            in [
                CLOCK,
                COUNTER,
            ]
            and state["red_end_orientation"] in [IN, OUT]
        ):
            for prop in self.scene.props.values():
                if prop.prop_type in strictly_placed_props:
                    self._set_strict_prop_location(prop)
                elif prop.prop_type in non_strictly_placed_props:
                    self._set_default_prop_location(prop)
        else:
            if red_end_location == blue_end_location:
                red_prop = next(
                    prop for prop in self.scene.props.values() if prop.color == RED
                )
                blue_prop = next(
                    prop for prop in self.scene.props.values() if prop.color == BLUE
                )

                red_direction = self._determine_translation_direction(
                    self.scene.motions[RED]
                )
                blue_direction = self._determine_translation_direction(
                    self.scene.motions[BLUE]
                )

                if red_direction:
                    self._move_prop(red_prop, red_direction)
                if blue_direction:
                    self._move_prop(blue_prop, blue_direction)

    ### BETA TO BETA ### G, H, I

    def _reposition_G_and_H(self, motion_df: pd.DataFrame) -> None:
        if self.scene_has_hybrid_orientation():
            self._set_default_prop_location(self.scene.props[RED])
            self._set_default_prop_location(self.scene.props[BLUE])
        else:
            further_direction = self._determine_translation_direction(
                self.scene.motions[RED]
            )
            other_direction = self._get_opposite_direction(further_direction)

            new_red_pos = self._calculate_new_position(
                self.scene.props[RED].pos(), further_direction
            )
            new_blue_pos = self._calculate_new_position(
                self.scene.props[BLUE].pos(), other_direction
            )

            self.scene.props[RED].setPos(new_red_pos)
            self.scene.props[BLUE].setPos(new_blue_pos)

    def scene_has_hybrid_orientation(self):
        return (
            self.red_prop.is_radial()
            and self.blue_prop.is_antiradial()
            or (self.red_prop.is_antiradial() and self.blue_prop.is_radial())
        )

    def _reposition_I(self, state) -> None:
        if (self.red_prop.is_radial() and self.blue_prop.is_antiradial()) or (
            self.red_prop.is_antiradial() and self.blue_prop.is_radial()
        ):
            for prop in self.scene.props.values():
                if prop.prop_type in strictly_placed_props:
                    self._set_strict_prop_location(prop)
                elif prop.prop_type in non_strictly_placed_props:
                    self._set_default_prop_location(prop)

        else:
            pro_prop = (
                self.scene.props[RED]
                if self.scene.motions[RED].motion_type == PRO
                else self.scene.props[BLUE]
            )
            anti_prop = (
                self.scene.props[RED]
                if self.scene.motions[RED].motion_type == ANTI
                else self.scene.props[BLUE]
            )

            pro_motion = self.scene.motions[pro_prop.color]

            pro_direction = self._determine_translation_direction(pro_motion)
            anti_direction = self._get_opposite_direction(pro_direction)

            new_position_pro = self._calculate_new_position(
                pro_prop.pos(), pro_direction
            )
            new_position_anti = self._calculate_new_position(
                anti_prop.pos(), anti_direction
            )

            pro_prop.setPos(new_position_pro)
            anti_prop.setPos(new_position_anti)

    def is_strict(self):
        return all(
            prop.prop_type in strictly_placed_props
            for prop in self.scene.props.values()
        )

    def is_not_strict(self):
        return all(
            prop.prop_type in non_strictly_placed_props
            for prop in self.scene.props.values()
        )

    ### GAMMA TO BETA ### Y, Z

    def reposition_gamma_to_beta(self) -> None:
        if self.scene.main_widget.prop_type in non_strictly_placed_props:
            if any(
                prop.orientation in [IN, OUT] for prop in self.scene.props.values()
            ) and any(
                prop.orientation in [CLOCK, COUNTER]
                for prop in self.scene.props.values()
            ):
                for prop in self.scene.props.values():
                    self._set_default_prop_location(prop)
            else:
                shift = (
                    self.scene.motions[RED]
                    if self.scene.motions[RED].motion_type in [PRO, ANTI]
                    else self.scene.motions[BLUE]
                )
                static_motion = (
                    self.scene.motions[RED]
                    if self.scene.motions[RED].motion_type == STATIC
                    else self.scene.motions[BLUE]
                )

                direction = self._determine_translation_direction(shift)
                if direction:
                    self._move_prop(
                        next(
                            prop
                            for prop in self.scene.props.values()
                            if prop.color == shift.color
                        ),
                        direction,
                    )
                    self._move_prop(
                        next(
                            prop
                            for prop in self.scene.props.values()
                            if prop.color == static_motion.color
                        ),
                        self._get_opposite_direction(direction),
                    )
        elif self.scene.main_widget.prop_type in strictly_placed_props:
            for prop in self.scene.props.values():
                self._set_strict_prop_location(prop)

    ### HELPERS ###

    def _determine_translation_direction(self, motion: Motion) -> Direction:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""

        is_shift = motion.motion_type in [
            PRO,
            ANTI,
            MotionType.FLOAT,
        ]
        is_static = motion.motion_type == STATIC

        if is_shift or is_static:
            if motion.prop.is_radial():
                if motion.end_location in [NORTH, SOUTH]:
                    if motion.start_location == EAST:
                        return RIGHT
                    elif motion.start_location == WEST:
                        return LEFT
                elif motion.end_location in [EAST, WEST]:
                    if motion.start_location == NORTH:
                        return UP
                    elif motion.start_location == SOUTH:
                        return DOWN

            elif motion.prop.is_antiradial():
                if motion.end_location in [NORTH, SOUTH]:
                    if motion.start_location == EAST:
                        return UP
                    elif motion.start_location == WEST:
                        return DOWN
                elif motion.end_location in [EAST, WEST]:
                    if motion.start_location == NORTH:
                        return RIGHT
                    elif motion.start_location == SOUTH:
                        return LEFT
            else:
                print(
                    "ERROR: Unrecognized Orientation -"
                    f"{motion.prop.orientation} -"
                    "Prop is neither radial nor antiradial"
                )

    def _props_in_beta(self) -> bool | None:
        visible_staves: List[Prop] = []
        for prop in self.scene.props.values():
            if prop.location:
                visible_staves.append(prop)
        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                return True
            else:
                return False

    def _calculate_new_position(
        self,
        current_position: QPointF,
        direction: Direction,
    ) -> QPointF:
        offset_map = {
            LEFT: QPointF(-BETA_OFFSET, 0),
            RIGHT: QPointF(BETA_OFFSET, 0),
            UP: QPointF(0, -BETA_OFFSET),
            DOWN: QPointF(0, BETA_OFFSET),
        }
        offset = offset_map.get(direction, QPointF(0, 0))
        return current_position + offset

    ### GETTERS

    def _get_position_offsets(self, prop: Prop) -> Dict[Tuple[str, str], QPointF]:
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()

        half_prop_width = prop_width / 2
        half_prop_length = prop_length / 2

        # Define a map for position offsets based on orientation and location
        position_offsets = {
            (IN, NORTH): QPointF(half_prop_width, -half_prop_length),
            (IN, SOUTH): QPointF(-half_prop_width, half_prop_length),
            (IN, EAST): QPointF(half_prop_length, half_prop_width),
            (IN, WEST): QPointF(-half_prop_length, -half_prop_width),
            (OUT, NORTH): QPointF(-half_prop_width, half_prop_length),
            (OUT, SOUTH): QPointF(half_prop_width, -half_prop_length),
            (OUT, EAST): QPointF(-half_prop_length, -half_prop_width),
            (OUT, WEST): QPointF(half_prop_length, half_prop_width),
            (CLOCK, NORTH): QPointF(-half_prop_length, -half_prop_width),
            (CLOCK, SOUTH): QPointF(half_prop_length, half_prop_width),
            (CLOCK, EAST): QPointF(half_prop_width, -half_prop_length),
            (CLOCK, WEST): QPointF(-half_prop_width, half_prop_length),
            (COUNTER, NORTH): QPointF(half_prop_length, half_prop_width),
            (COUNTER, SOUTH): QPointF(-half_prop_length, -half_prop_width),
            (COUNTER, EAST): QPointF(-half_prop_width, half_prop_length),
            (COUNTER, WEST): QPointF(half_prop_width, -half_prop_length),
        }
        return position_offsets

    def _get_opposite_direction(self, movement: Direction) -> Direction:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
        }
        return opposite_directions.get(movement)
