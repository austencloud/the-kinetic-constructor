from PyQt6.QtCore import QPointF
import math

import pandas as pd
from constants.numerical_constants import BETA_OFFSET
from constants.string_constants import (
    BOX,
    BUUGENG,
    CLOCKWISE,
    CLUB,
    COUNTER_CLOCKWISE,
    DIAMOND,
    DOUBLESTAR,
    BIGDOUBLESTAR,
    FAN,
    MINIHOOP,
    BIGHOOP,
    IN,
    OUT,
    COLOR,
    STAFF,
    BIGSTAFF,
    QUIAD,
    GUITAR,
    SWORD,
    UKULELE,
    CHICKEN,
    STATIC,
    PRO,
    ANTI,
    NORTH,
    SOUTH,
    EAST,
    TRIAD,
    BIGTRIAD,
    WEST,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    RED,
    BLUE,
)
from typing import TYPE_CHECKING, Dict, List, Tuple
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    LetterDictionary,
    OptimalLocationsEntries,
    OptimalLocationsDicts,
    Direction,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class PropPositioner:
    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.letters: LetterDictionary = scene.main_widget.letters

    def update_prop_positions(self) -> None:
        self.prop_type_counts = self.count_prop_types()
        for prop in self.scene.props.values():
            if any(
                self.prop_type_counts[ptype] == 2
                for ptype in [BIGHOOP, DOUBLESTAR, BIGTRIAD, BIGDOUBLESTAR]
            ):
                self.set_strict_prop_locations(prop)
            else:
                self.set_default_prop_locations(prop)

        for prop in self.scene.ghost_props.values():
            if any(
                self.prop_type_counts[ptype] == 2
                for ptype in [BIGHOOP, DOUBLESTAR, BIGTRIAD, BIGDOUBLESTAR]
            ):
                self.set_strict_prop_locations(prop)
            else:
                self.set_default_prop_locations(prop)

        if self.props_in_beta():
            self.reposition_beta_props()

    def count_prop_types(self) -> Dict[str, int]:
        prop_types = [
            BIGHOOP,
            DOUBLESTAR,
            BIGDOUBLESTAR,
            STAFF,
            BIGSTAFF,
            FAN,
            CLUB,
            BUUGENG,
            MINIHOOP,
            TRIAD,
            BIGTRIAD,
            QUIAD,
            SWORD,
            GUITAR,
            UKULELE,
            CHICKEN,
        ]
        return {
            ptype: sum(prop.prop_type == ptype for prop in self.scene.props.values())
            for ptype in prop_types
        }

    def set_strict_prop_locations(self, prop: "Prop") -> None:
        position_offsets = self.get_position_offsets(prop)
        key = (prop.orientation, prop.location)
        offset = position_offsets.get(key, QPointF(0, 0))
        prop.setTransformOriginPoint(0, 0)
        if self.scene.grid.grid_mode == DIAMOND:
            if prop.location in self.scene.grid.strict_diamond_hand_points:
                prop.setPos(
                    self.scene.grid.strict_diamond_hand_points[prop.location] + offset
                )

    def set_default_prop_locations(self, prop: "Prop") -> None:
        position_offsets = self.get_position_offsets(prop)
        key = (prop.orientation, prop.location)
        offset = position_offsets.get(key, QPointF(0, 0))
        prop.setTransformOriginPoint(0, 0)
        if self.scene.grid.grid_mode == DIAMOND:
            if prop.location in self.scene.grid.diamond_hand_points:
                prop.setPos(self.scene.grid.diamond_hand_points[prop.location] + offset)
        elif self.scene.grid.grid_mode == BOX:
            if prop.location in self.scene.grid.box_hand_points:
                prop.setPos(self.scene.grid.box_hand_points[prop.location] + offset)

    def get_position_offsets(self, prop: Prop) -> Dict[Tuple[str, str], QPointF]:
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()

        # Define a map for position offsets based on orientation and location
        position_offsets = {
            (IN, NORTH): QPointF(prop_width / 2, -prop_length / 2),
            (IN, SOUTH): QPointF(-prop_width / 2, prop_length / 2),
            (IN, EAST): QPointF(prop_length / 2, prop_width / 2),
            (IN, WEST): QPointF(-prop_length / 2, -prop_width / 2),
            (OUT, NORTH): QPointF(-prop_width / 2, prop_length / 2),
            (OUT, SOUTH): QPointF(prop_width / 2, -prop_length / 2),
            (OUT, EAST): QPointF(-prop_length / 2, -prop_width / 2),
            (OUT, WEST): QPointF(prop_length / 2, prop_width / 2),
            (CLOCKWISE, NORTH): QPointF(-prop_length / 2, -prop_width / 2),
            (CLOCKWISE, SOUTH): QPointF(prop_length / 2, prop_width / 2),
            (CLOCKWISE, EAST): QPointF(prop_width / 2, -prop_length / 2),
            (CLOCKWISE, WEST): QPointF(-prop_width / 2, prop_length / 2),
            (COUNTER_CLOCKWISE, NORTH): QPointF(prop_length / 2, prop_width / 2),
            (COUNTER_CLOCKWISE, SOUTH): QPointF(-prop_length / 2, -prop_width / 2),
            (COUNTER_CLOCKWISE, EAST): QPointF(-prop_width / 2, prop_length / 2),
            (COUNTER_CLOCKWISE, WEST): QPointF(prop_width / 2, -prop_length / 2),
        }
        return position_offsets

    def move_prop(self, prop: Prop, direction: Direction) -> None:
        new_position = self.calculate_new_position(prop.pos(), direction)
        prop.setPos(new_position)


    ### REPOSITIONING ###

    def reposition_beta_props(self) -> None:
        state = self.scene.get_state()  # Now a dictionary

        # Gather motions by type
        pro_or_anti_motions = [
            color
            for color in [RED, BLUE]
            if state[f"{color}_motion_type"] in [PRO, ANTI]
        ]
        static_motions = [
            color for color in [RED, BLUE] if state[f"{color}_motion_type"] == STATIC
        ]

        # STATIC BETA - β
        if len(static_motions) > 1:
            self.reposition_static_beta(static_motions)

        # BETA to BETA - G, H, I
        if (
            state["red_start_location"] == state["blue_start_location"]
            and state["red_end_location"] == state["blue_end_location"]
        ):
            self.reposition_beta_to_beta(state)

        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_motions) == 1 and len(static_motions) == 1:
            self.reposition_gamma_to_beta(pro_or_anti_motions, static_motions)

        # ALPHA → BETA - D, E, F
        if all(state[f"{color}_motion_type"] != STATIC for color in [RED, BLUE]):
            if state["red_start_location"] != state["blue_start_location"]:
                self.reposition_alpha_to_beta(state)

    ### STATIC BETA ### β

    def reposition_static_beta(self, move_prop: callable, static_motions: Dict) -> None:
        for color, motion in static_motions.items():
            prop = next(
                (p for p in self.scene.props.values() if p.color == color), None
            )
            if not prop:
                continue
            other_prop = next(
                (
                    other
                    for other in self.scene.props.values()
                    if other != prop and other.location == prop.location
                ),
                None,
            )
            if other_prop and other_prop.layer != prop.layer:
                if prop.prop_type in [
                    STAFF,
                    FAN,
                    CLUB,
                    BUUGENG,
                    MINIHOOP,
                    TRIAD,
                    QUIAD,
                    UKULELE,
                    CHICKEN,
                ]:
                    self.set_default_prop_locations(prop)
                elif prop.prop_type in [
                    DOUBLESTAR,
                    BIGHOOP,
                    BIGDOUBLESTAR,
                    BIGSTAFF,
                    SWORD,
                    GUITAR,
                ]:
                    self.set_strict_prop_locations(other_prop)
            else:
                end_location = motion[f"{color}_end_location"]
                direction = self.determine_direction_for_static_beta(prop, end_location)
                if direction:
                    move_prop(prop, direction)

    def determine_direction_for_static_beta(
        self, prop: Prop, end_location: str
    ) -> Direction | None:
        layer_reposition_map = {
            1: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP if end_location == EAST else None,
                (WEST, BLUE): DOWN if end_location == WEST else None,
                (WEST, RED): UP if end_location == WEST else None,
                (EAST, BLUE): DOWN if end_location == EAST else None,
            },
            2: {
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

        return layer_reposition_map[prop.layer].get((prop.location, prop.color), None)

    ### ALPHA TO BETA ### D, E, F

    def reposition_alpha_to_beta(self, state) -> None:
        # Extract motion type and end locations for both colors from the DataFrame row
        red_motion_type = state["red_motion_type"]
        blue_motion_type = state["blue_motion_type"]
        red_end_location = state["red_end_location"]
        blue_end_location = state["blue_end_location"]

        # We assume red and blue are always present, and determine direction based on the end locations
        if red_end_location == blue_end_location:
            # Get the props associated with the colors
            red_prop = next(
                prop for prop in self.scene.props.values() if prop.color == RED
            )
            blue_prop = next(
                prop for prop in self.scene.props.values() if prop.color == BLUE
            )

            # Determine the direction for repositioning based on the motion type and locations
            red_direction = self.determine_translation_direction(
                red_motion_type,
                state[f"{RED}_start_location"],
                red_end_location,
                state[f"{RED}_end_layer"],
            )
            blue_direction = self.determine_translation_direction(
                blue_motion_type,
                state[f"{BLUE}_start_location"],
                blue_end_location,
                state[f"{BLUE}_end_layer"],
            )

            # If there's a valid direction, move the props accordingly
            if red_direction:
                self.move_prop(red_prop, red_direction)
            if blue_direction:
                self.move_prop(blue_prop, blue_direction)

    ### BETA TO BETA ### G, H, I

    def reposition_beta_to_beta(self, motions: Dict) -> None:
        same_motion_type = (
            motions["red_motion_type"] == motions["blue_motion_type"] in [PRO, ANTI]
        )
        if same_motion_type:
            self.reposition_G_and_H(motions)
        else:
            self.reposition_I(motions)

    def reposition_G_and_H(self, motion_df: pd.DataFrame) -> None:
        # Determine directions for motion
        further_direction = self.determine_translation_direction(
            motion_df[f"red_motion_type"],
            motion_df[f"red_start_location"],
            motion_df[f"red_end_location"],
            motion_df[f"red_end_layer"],
        )
        other_direction = self.get_opposite_direction(further_direction)

        # Calculate new positions
        new_red_pos = self.calculate_new_position(
            self.scene.props[RED].pos(), further_direction
        )
        new_blue_pos = self.calculate_new_position(
            self.scene.props[BLUE].pos(), other_direction
        )

        # Update positions
        self.scene.props[RED].setPos(new_red_pos)
        self.scene.props[BLUE].setPos(new_blue_pos)

    def reposition_I(self, motions_df) -> None:
        if all(
            prop.prop_type in [CLUB, FAN, TRIAD, MINIHOOP, UKULELE, CHICKEN]
            for prop in self.scene.props.values()
        ):
            for prop in self.scene.props.values():
                self.set_default_prop_locations(prop)
        elif all(
            prop.prop_type in [BIGHOOP, BIGTRIAD, SWORD, GUITAR]
            for prop in self.scene.props.values()
        ):
            for prop in self.scene.props.values():
                self.set_strict_prop_locations(prop)
        else:
            pro_color = RED if motions_df[f"{RED}_motion_type"] == PRO else BLUE
            anti_color = RED if pro_color == BLUE else BLUE

            pro_prop = next(
                prop
                for prop in self.scene.props.values()
                if prop.motion.motion_type == PRO
            )
            anti_prop = next(
                prop
                for prop in self.scene.props.values()
                if prop.motion.motion_type == ANTI
            )

            pro_motion_df = {
                f"{pro_color}_motion_type": motions_df[f"{pro_color}_motion_type"],
                f"{pro_color}_start_location": motions_df[
                    f"{pro_color}_start_location"
                ],
                f"{pro_color}_end_location": motions_df[f"{pro_color}_end_location"],
                f"{pro_color}_end_layer": motions_df[f"{pro_color}_end_layer"],
            }

            pro_direction = self.determine_translation_direction(
                pro_motion_df[f"{pro_color}_motion_type"],
                pro_motion_df[f"{pro_color}_start_location"],
                pro_motion_df[f"{pro_color}_end_location"],
                pro_motion_df[f"{pro_color}_end_layer"],
            )
            anti_direction = self.get_opposite_direction(pro_direction)

            new_position_pro = self.calculate_new_position(
                pro_prop.pos(), pro_direction
            )
            new_position_anti = self.calculate_new_position(
                anti_prop.pos(), anti_direction
            )

            pro_prop.setPos(new_position_pro)
            anti_prop.setPos(new_position_anti)

    ### GAMMA TO BETA ### Y, Z

    def reposition_gamma_to_beta(self, move_prop, shifts, static_motions) -> None:
        if self.scene.prop_type in [
            STAFF,
            FAN,
            CLUB,
            BUUGENG,
            MINIHOOP,
            TRIAD,
            QUIAD,
            UKULELE,
            CHICKEN,
        ]:
            if any(prop.layer == 1 for prop in self.scene.props.values()) and any(
                prop.layer == 2 for prop in self.scene.props.values()
            ):
                for prop in self.scene.props.values():
                    self.set_default_prop_locations(prop)
            else:
                shift, static_motion = shifts[0], static_motions[0]
                direction = self.determine_translation_direction(shift)
                if direction:
                    move_prop(
                        next(
                            prop
                            for prop in self.scene.props.values()
                            if prop.color == shift[COLOR]
                        ),
                        direction,
                    )
                    move_prop(
                        next(
                            prop
                            for prop in self.scene.props.values()
                            if prop.color == static_motion[COLOR]
                        ),
                        self.get_opposite_direction(direction),
                    )
        elif self.scene.prop_type in [
            BIGHOOP,
            BIGSTAFF,
            DOUBLESTAR,
            BIGDOUBLESTAR,
            SWORD,
            GUITAR,
            BIGTRIAD,
        ]:
            for prop in self.scene.props.values():
                self.set_strict_prop_locations(prop)

    ### HELPERS ###

    def props_in_beta(self) -> bool | None:
        visible_staves: List[Prop] = []
        for prop in self.scene.props.values():
            if prop.location:
                visible_staves.append(prop)
        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                return True
            else:
                return False

    def find_optimal_arrow_location_entry(
        self,
        current_state,
        matching_letters_df,
        arrow_dict,
    ) -> OptimalLocationsEntries | None:
        for candidate_state in matching_letters_df:
            # convert candidate_state to a dataframe called candidate_state_df
            candidate_state_df = pd.DataFrame(candidate_state, index=[0])
            if self.scene.arrow_positioner.compare_states(
                current_state, candidate_state_df
            ):
                optimal_entry: OptimalLocationsDicts = next(
                    (
                        d
                        for d in candidate_state
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict[COLOR]}_location"
                    return optimal_entry.get(color_key)
        return None

    def determine_translation_direction(
        self, motion_type, start_location, end_location, end_layer
    ) -> Direction:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if end_layer == 1 and motion_type in [PRO, ANTI, STATIC]:
            if end_location in [NORTH, SOUTH]:
                return RIGHT if start_location == EAST else LEFT
            elif end_location in [EAST, WEST]:
                return DOWN if start_location == SOUTH else UP
        elif end_layer == 2 and motion_type in [PRO, ANTI, STATIC]:
            if end_location in [NORTH, SOUTH]:
                return UP if start_location == EAST else DOWN
            elif end_location in [EAST, WEST]:
                return RIGHT if start_location == SOUTH else LEFT

    def calculate_new_position(
        self,
        current_position: QPointF,
        direction: Direction,
    ) -> QPointF:
        offset = (
            QPointF(BETA_OFFSET, 0)
            if direction in [LEFT, RIGHT]
            else QPointF(0, BETA_OFFSET)
        )
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        elif direction in [LEFT, UP]:
            return current_position - offset
        else:
            return current_position

    ### GETTERS

    def get_distance_from_center(self, arrow_pos: Dict[str, float]) -> float:
        grid_center = self.scene.grid.center
        arrow_x, arrow_y = arrow_pos.get("x", 0.0), arrow_pos.get("y", 0.0)
        center_x, center_y = grid_center.x(), grid_center.y()

        distance_from_center = math.sqrt(
            (arrow_x - center_x) ** 2 + (arrow_y - center_y) ** 2
        )
        return distance_from_center

    def get_optimal_arrow_location(
        self, state: pd.Series, color: str
    ) -> Dict[str, float] | None:
        # Get the current state and letter
        current_state = self.scene.get_state()
        current_letter = self.scene.current_letter

        if current_letter is not None:
            matching_letters = self.letters[current_letter]

            # Find the optimal location entry
            optimal_entry = self.find_optimal_arrow_location_entry(
                current_state, matching_letters, state
            )

            # Extract the optimal location for the specified color
            if optimal_entry:
                color_key = f"optimal_{color}_location"
                return optimal_entry.get(color_key)

        return None

    def get_opposite_direction(self, movement: Direction) -> Direction:
        if movement == LEFT:
            return RIGHT
        elif movement == RIGHT:
            return LEFT
        elif movement == UP:
            return DOWN
        elif movement == DOWN:
            return UP
