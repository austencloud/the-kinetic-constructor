from PyQt6.QtCore import QPointF
import math
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
    MOTION_TYPE,
    STAFF,
    BIGSTAFF,
    QUIAD,
    GUITAR,
    SWORD,
    STATIC,
    START_LOCATION,
    END_LOCATION,
    PRO,
    ANTI,
    NORTH,
    SOUTH,
    EAST,
    TRIAD,
    WEST,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    RED,
    BLUE,
    END_LAYER,
)
from typing import TYPE_CHECKING, Dict, List
from objects.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    MotionAttributesDicts,
    LetterDictionary,
    OptimalLocationsEntries,
    OptimalLocationsDicts,
    Direction,
    Locations,
)

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class PropPositioner:
    current_state: List[MotionAttributesDicts]
    matching_letters: List[LetterDictionary]
    arrow_dict: List[MotionAttributesDicts]
    letters: LetterDictionary

    def __init__(self, scene: "Pictograph") -> None:
        self.scene = scene
        self.view = scene.view
        self.letters = scene.letters

    def update_prop_positions(self) -> None:
        # Dictionary to store the count of each prop type
        self.prop_type_counts = {
            BIGHOOP: 0,
            DOUBLESTAR: 0,
            BIGDOUBLESTAR: 0,
            STAFF: 0,
            BIGSTAFF: 0,
            FAN: 0,
            CLUB: 0,
            BUUGENG: 0,
            MINIHOOP: 0,
            TRIAD: 0,
            QUIAD: 0,
            SWORD: 0,
            GUITAR: 0,
            "???": 0,
        }

        # First pass to count prop types
        for prop in self.scene.props:
            if prop.prop_type == BIGHOOP:
                self.prop_type_counts[BIGHOOP] += 1
            elif prop.prop_type == DOUBLESTAR:
                self.prop_type_counts[DOUBLESTAR] += 1
            elif prop.prop_type == BIGDOUBLESTAR:
                self.prop_type_counts[BIGDOUBLESTAR] += 1
            elif prop.prop_type == STAFF:
                self.prop_type_counts[STAFF] += 1
            elif prop.prop_type == BIGSTAFF:
                self.prop_type_counts[BIGSTAFF] += 1
            elif prop.prop_type == FAN:
                self.prop_type_counts[FAN] += 1
            elif prop.prop_type == CLUB:
                self.prop_type_counts[CLUB] += 1
            elif prop.prop_type == BUUGENG:
                self.prop_type_counts[BUUGENG] += 1
            elif prop.prop_type == MINIHOOP:
                self.prop_type_counts[MINIHOOP] += 1
            elif prop.prop_type == TRIAD:
                self.prop_type_counts[TRIAD] += 1
            elif prop.prop_type == QUIAD:
                self.prop_type_counts[QUIAD] += 1
            elif prop.prop_type == SWORD:
                self.prop_type_counts[SWORD] += 1
            elif prop.prop_type == GUITAR:
                self.prop_type_counts[GUITAR] += 1
            else:
                self.prop_type_counts["???"] += 1

        for prop in self.scene.props:
            if (
                self.prop_type_counts[BIGHOOP] == 2
                or self.prop_type_counts[DOUBLESTAR] == 2
                or self.prop_type_counts[BIGDOUBLESTAR] == 2
            ):
                self.set_strict_prop_locations(prop)
            else:
                self.set_default_prop_locations(prop)

        if self.props_in_beta():
            self.reposition_beta_props()

    def set_strict_prop_locations(self, prop: "Prop") -> None:
        prop.setTransformOriginPoint(0, 0)
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

        if self.scene.grid.grid_mode == DIAMOND:
            if prop.prop_location in self.scene.grid.strict_diamond_hand_points:
                key = (prop.orientation, prop.prop_location)
                offset = position_offsets.get(key, QPointF(0, 0))
                prop.setPos(
                    self.scene.grid.strict_diamond_hand_points[prop.prop_location]
                    + offset
                )

    def set_default_prop_locations(self, prop: "Prop") -> None:
        prop.setTransformOriginPoint(0, 0)
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

        if self.scene.grid.grid_mode == DIAMOND:
            if prop.prop_location in self.scene.grid.diamond_hand_points:
                key = (prop.orientation, prop.prop_location)
                offset = position_offsets.get(key, QPointF(0, 0))  # Default offset
                prop.setPos(
                    self.scene.grid.diamond_hand_points[prop.prop_location] + offset
                )

        elif self.scene.grid.grid_mode == BOX:
            if prop.prop_location in self.scene.grid.box_hand_points:
                key = (prop.orientation, prop.prop_location)
                offset = position_offsets.get(key, QPointF(0, 0))  # Default offset
                prop.setPos(
                    self.scene.grid.box_hand_points[prop.prop_location] + offset
                )

    def reposition_beta_props(self) -> None:
        board_state = self.scene.get_state()

        def move_prop(prop: Prop, direction) -> None:
            new_position = self.calculate_new_position(prop.pos(), direction)
            prop.setPos(new_position)

        motions_grouped_by_start_loc: Dict[Locations, List[MotionAttributesDicts]] = {}
        for motion in board_state:
            motions_grouped_by_start_loc.setdefault(motion[START_LOCATION], []).append(
                motion
            )

        pro_or_anti_motions = [
            motion for motion in board_state if motion[MOTION_TYPE] in [PRO, ANTI]
        ]
        static_motions = [
            motion for motion in board_state if motion[MOTION_TYPE] == STATIC
        ]

        # STATIC BETA
        if len(static_motions) > 1:
            self.reposition_static_beta(move_prop, static_motions)

        # BETA → BETA - G, H, I
        for start_location, motions in motions_grouped_by_start_loc.items():
            if len(motions) == 2:
                motion1, motion2 = motions
                if (
                    motion1[START_LOCATION] == motion2[START_LOCATION]
                    and motion1[END_LOCATION] == motion2[END_LOCATION]
                ):
                    if motion1[MOTION_TYPE] in [PRO, ANTI]:
                        if motion2[MOTION_TYPE] in [PRO, ANTI]:
                            self.reposition_beta_to_beta(motions)

        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_motions) == 1 and len(static_motions) == 1:
            # if all the staves are in layer 1 or layer 2
            if all(prop.layer == 1 for prop in self.scene.props) or all(
                prop.layer == 2 for prop in self.scene.props
            ):
                self.reposition_gamma_to_beta(
                    move_prop, pro_or_anti_motions, static_motions
                )

        # ALPHA → BETA - D, E, F
        converging_motions = [
            motion for motion in board_state if motion[MOTION_TYPE] not in [STATIC]
        ]
        if len(converging_motions) == 2:
            if converging_motions[0].get(START_LOCATION) != converging_motions[1].get(
                START_LOCATION
            ):
                if all(prop.layer == 1 for prop in self.scene.props) or all(
                    prop.layer == 2 for prop in self.scene.props
                ):
                    self.reposition_alpha_to_beta(move_prop, converging_motions)

    ### STATIC BETA ### β

    def reposition_static_beta(
        self, move_prop: callable, static_motions: List[MotionAttributesDicts]
    ) -> None:
        # if there's a combination of a BIGHOOP and a CLUB in the prop_type_counts dictionary
        if self.prop_type_counts[BIGHOOP] == 1 and self.prop_type_counts[CLUB] == 1:
            # set both props to their default locations, strict for big hoop and default for club
            for prop in self.scene.props:
                if prop.prop_type == BIGHOOP:
                    self.set_strict_prop_locations(prop)
                elif prop.prop_type == CLUB:
                    self.set_default_prop_locations(prop)

        else:
            for motion in static_motions:
                prop = next(
                    (prop for prop in self.scene.props if prop.color == motion[COLOR]),
                    None,
                )
                if not prop:
                    continue

                # Check if there's another prop at the same location but in a different layer
                other_prop = next(
                    (
                        other
                        for other in self.scene.props
                        if other != prop and other.prop_location == prop.prop_location
                    ),
                    None,
                )

                # If the other prop is in a different layer, set both props to default locations
                if other_prop and other_prop.layer != prop.layer:
                    if prop.prop_type in [STAFF, FAN, CLUB, BUUGENG, MINIHOOP, TRIAD, QUIAD]:
                        self.set_default_prop_locations(prop)
                    elif prop.prop_type in [DOUBLESTAR, BIGHOOP, BIGDOUBLESTAR, BIGSTAFF, SWORD, GUITAR]:
                        self.set_strict_prop_locations(other_prop)
                else:
                    # Original logic for handling props in the same layer
                    end_location = motion[END_LOCATION]
                    direction = self.determine_direction_for_static_beta(
                        prop, end_location
                    )
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

        return layer_reposition_map[prop.layer].get(
            (prop.prop_location, prop.color), None
        )

    ### ALPHA TO BETA ### D, E, F

    def reposition_alpha_to_beta(self, move_prop, converging_arrows) -> None:
        # check if all the props are in layer 1
        if all(prop.layer == 1 for prop in self.scene.props):
            end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
            start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
            if (
                end_locations[0] == end_locations[1]
                and start_locations[0] != start_locations[1]
            ):
                for arrow in converging_arrows:
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        move_prop(
                            next(
                                prop
                                for prop in self.scene.props
                                if prop.color == arrow[COLOR]
                            ),
                            direction,
                        )
        # check if all the props are in layer 2
        elif all(prop.layer == 2 for prop in self.scene.props):
            end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
            start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
            if (
                end_locations[0] == end_locations[1]
                and start_locations[0] != start_locations[1]
            ):
                for arrow in converging_arrows:
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        move_prop(
                            next(
                                prop
                                for prop in self.scene.props
                                if prop.arrow.color == arrow[COLOR]
                            ),
                            direction,
                        )
        # check if one prop is in layer 1 and the other is in layer 2
        elif any(prop.layer == 1 for prop in self.scene.props) and any(
            prop.layer == 2 for prop in self.scene.props
        ):
            end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
            start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
            if (
                end_locations[0] == end_locations[1]
                and start_locations[0] != start_locations[1]
            ):
                for arrow in converging_arrows:
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        move_prop(
                            next(
                                prop
                                for prop in self.scene.props
                                if prop.arrow.color == arrow[COLOR]
                            ),
                            direction,
                        )

    ### BETA TO BETA ### G, H, I

    def reposition_beta_to_beta(self, motions) -> None:
        motion1, motion2 = motions
        same_motion_type = motion1[MOTION_TYPE] == motion2[MOTION_TYPE] in [PRO, ANTI]

        if same_motion_type:
            self.reposition_G_and_H(motion1, motion2)
        else:
            self.reposition_I(motion1, motion2)

    def reposition_G_and_H(self, motion1, motion2) -> None:
        optimal_location1 = self.get_optimal_arrow_location(motion1)
        optimal_location2 = self.get_optimal_arrow_location(motion2)

        if not optimal_location1 or not optimal_location2:
            return

        distance1 = self.get_distance_from_center(optimal_location1)
        distance2 = self.get_distance_from_center(optimal_location2)

        further_arrow = motion1 if distance1 > distance2 else motion2
        other_arrow = motion1 if further_arrow == motion2 else motion2

        further_direction = self.determine_translation_direction(further_arrow)

        further_prop = next(
            prop
            for prop in self.scene.props
            if prop.arrow.color == further_arrow[COLOR]
        )
        new_position_further = self.calculate_new_position(
            further_prop.pos(), further_direction
        )
        further_prop.setPos(new_position_further)

        other_direction = self.get_opposite_direction(further_direction)
        other_prop = next(
            prop for prop in self.scene.props if prop.arrow.color == other_arrow[COLOR]
        )
        new_position_other = self.calculate_new_position(
            other_prop.pos(), other_direction
        )
        other_prop.setPos(new_position_other)

    def reposition_I(self, motion1, motion2) -> None:
        pro_motion = motion1 if motion1[MOTION_TYPE] == PRO else motion2
        anti_motion = motion2 if motion1[MOTION_TYPE] == PRO else motion1

        pro_prop = next(
            (
                prop
                for prop in self.scene.props
                if prop.arrow.color == pro_motion[COLOR]
            ),
            None,
        )
        anti_prop = next(
            (
                prop
                for prop in self.scene.props
                if prop.arrow.color == anti_motion[COLOR]
            ),
            None,
        )

        if pro_prop and anti_prop:
            pro_prop_translation_direction = self.determine_translation_direction(
                pro_motion
            )
            anti_prop_translation_direction = self.get_opposite_direction(
                pro_prop_translation_direction
            )

            new_position_pro = self.calculate_new_position(
                pro_prop.pos(), pro_prop_translation_direction
            )
            pro_prop.setPos(new_position_pro)

            new_position_anti = self.calculate_new_position(
                anti_prop.pos(), anti_prop_translation_direction
            )
            anti_prop.setPos(new_position_anti)

    ### GAMMA TO BETA ### Y, Z

    def reposition_gamma_to_beta(self, move_prop, shifts, static_motions) -> None:
        if self.scene.prop_type in [
            STAFF,
            BIGSTAFF,
            FAN,
            CLUB,
            BUUGENG,
            MINIHOOP,
            TRIAD,
            QUIAD,
            DOUBLESTAR,
            BIGDOUBLESTAR,
            SWORD, GUITAR
        ]:
            if any(prop.layer == 1 for prop in self.scene.props) and any(
                prop.layer == 2 for prop in self.scene.props
            ):
                for prop in self.scene.props:
                    self.set_default_prop_locations(prop)
            else:
                shift, static_motion = shifts[0], static_motions[0]
                direction = self.determine_translation_direction(shift)
                if direction:
                    move_prop(
                        next(
                            prop
                            for prop in self.scene.props
                            if prop.arrow.color == shift[COLOR]
                        ),
                        direction,
                    )
                    move_prop(
                        next(
                            prop
                            for prop in self.scene.props
                            if prop.arrow.color == static_motion[COLOR]
                        ),
                        self.get_opposite_direction(direction),
                    )
        elif self.scene.prop_type in [BIGHOOP]:
            for prop in self.scene.props:
                self.set_strict_prop_locations(prop)

    ### HELPERS ###

    def props_in_beta(self) -> bool | None:
        visible_staves: List[Prop] = []
        for prop in self.scene.props:
            if prop.isVisible():
                visible_staves.append(prop)
        if len(visible_staves) == 2:
            if visible_staves[0].prop_location == visible_staves[1].prop_location:
                return True
            else:
                return False

    def find_optimal_arrow_location_entry(
        self,
        current_state,
        matching_letters,
        arrow_dict,
    ) -> OptimalLocationsEntries | None:
        for variants in matching_letters:
            if self.scene.arrow_positioner.compare_states(current_state, variants):
                optimal_entry: OptimalLocationsDicts = next(
                    (
                        d
                        for d in variants
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict[COLOR]}_location"
                    return optimal_entry.get(color_key)
        return None

    def determine_translation_direction(self, motion) -> Direction:
        """Determine the translation direction based on the arrow's board_state."""
        if motion[END_LAYER] == 1 and motion[MOTION_TYPE] in [PRO, ANTI, STATIC]:
            if motion[END_LOCATION] in [NORTH, SOUTH]:
                return RIGHT if motion[START_LOCATION] == EAST else LEFT
            elif motion[END_LOCATION] in [EAST, WEST]:
                return DOWN if motion[START_LOCATION] == SOUTH else UP
        elif motion[END_LAYER] == 2 and motion[MOTION_TYPE] in [PRO, ANTI, STATIC]:
            if motion[END_LOCATION] in [NORTH, SOUTH]:
                return UP if motion[START_LOCATION] == EAST else DOWN
            elif motion[END_LOCATION] in [EAST, WEST]:
                return RIGHT if motion[START_LOCATION] == SOUTH else LEFT

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
        self, arrow_attributes: ArrowAttributesDicts
    ) -> Dict[str, float] | None:
        current_state = self.scene.get_state()
        current_letter = self.scene.current_letter

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location_entry(
                current_state, matching_letters, arrow_attributes
            )
            if optimal_location:
                return optimal_location
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
