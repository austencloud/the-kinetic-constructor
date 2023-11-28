from PyQt6.QtCore import QPointF
import math
from settings.numerical_constants import BETA_OFFSET, STAFF_LENGTH, STAFF_WIDTH
from settings.string_constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    HORIZONTAL,
    IN,
    OUT,
    VERTICAL,
    COLOR,
    MOTION_TYPE,
    STATIC,
    START_LOCATION,
    END_LOCATION,
    PRO,
    ANTI,
    NORTH,
    SOUTH,
    EAST,
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
from objects.props.staff import Staff
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    MotionAttributesDicts,
    LetterDictionary,
    OptimalLocationEntries,
    OptimalLocationsDicts,
    Direction,
    Location,
)

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class StaffPositioner:
    current_state: List[MotionAttributesDicts]
    matching_letters: List[LetterDictionary]
    arrow_dict: List[MotionAttributesDicts]
    letters: LetterDictionary

    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.view = pictograph.view
        self.letters = pictograph.letters

    def update(self) -> None:
        for staff in self.pictograph.props:
            self.set_default_staff_locations(staff)
        if self.staffs_in_beta():
            self.reposition_beta_staffs()

    def set_default_staff_locations(self, staff: "Staff") -> None:
        staff.setTransformOriginPoint(0, 0)
        staff_length = staff.boundingRect().width()
        staff_width = staff.boundingRect().height()

        # Define a mapping for position offsets based on orientation and location
        position_offsets = {
            (IN, NORTH): QPointF(staff_width / 2, -staff_length / 2),
            (IN, SOUTH): QPointF(-staff_width / 2, staff_length / 2),
            (IN, EAST): QPointF(staff_length / 2, staff_width / 2),
            (IN, WEST): QPointF(-staff_length / 2, -staff_width / 2),
            (OUT, NORTH): QPointF(-staff_width / 2, staff_length / 2),
            (OUT, SOUTH): QPointF(staff_width / 2, -staff_length / 2),
            (OUT, EAST): QPointF(-staff_length / 2, -staff_width / 2),
            (OUT, WEST): QPointF(staff_length / 2, staff_width / 2),
            (CLOCKWISE, NORTH): QPointF(-staff_length / 2, -staff_width / 2),
            (CLOCKWISE, SOUTH): QPointF(staff_length / 2, staff_width / 2),
            (CLOCKWISE, EAST): QPointF(staff_width / 2, -staff_length / 2),
            (CLOCKWISE, WEST): QPointF(-staff_width / 2, staff_length / 2),
            (COUNTER_CLOCKWISE, NORTH): QPointF(staff_length / 2, staff_width / 2),
            (COUNTER_CLOCKWISE, SOUTH): QPointF(-staff_length / 2, -staff_width / 2),
            (COUNTER_CLOCKWISE, EAST): QPointF(-staff_width / 2, staff_length / 2),
            (COUNTER_CLOCKWISE, WEST): QPointF(staff_width / 2, -staff_length / 2),
        }

        if staff.location in self.pictograph.grid.handpoints:
            key = (staff.orientation, staff.location)
            offset = position_offsets.get(key, QPointF(0, 0))  # Default offset
            staff.setPos(self.pictograph.grid.handpoints[staff.location] + offset)

    def reposition_beta_staffs(self) -> None:
        board_state = self.pictograph.get_state()

        def move_staff(staff: Staff, direction) -> None:
            new_position = self.calculate_new_position(staff.pos(), direction)
            staff.setPos(new_position)

        motions_grouped_by_start_loc: Dict[Location, List[MotionAttributesDicts]] = {}
        for motion in board_state:
            motions_grouped_by_start_loc.setdefault(motion[START_LOCATION], []).append(
                motion
            )

        pro_or_anti_arrows = [
            arrow for arrow in board_state if arrow[MOTION_TYPE] in [PRO, ANTI]
        ]
        static_motions = [
            arrow for arrow in board_state if arrow[MOTION_TYPE] == STATIC
        ]

        # STATIC BETA
        if len(static_motions) > 1:
            self.reposition_static_beta(move_staff, static_motions)

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
        if len(pro_or_anti_arrows) == 1 and len(static_motions) == 1:
            self.reposition_gamma_to_beta(
                move_staff, pro_or_anti_arrows, static_motions
            )

        # ALPHA → BETA - D, E, F
        converging_motions = [
            motion for motion in board_state if motion[MOTION_TYPE] not in [STATIC]
        ]
        if len(converging_motions) == 2:
            if converging_motions[0].get(START_LOCATION) != converging_motions[1].get(
                START_LOCATION
            ):
                self.reposition_alpha_to_beta(move_staff, converging_motions)

    ### STATIC BETA ### β

    def reposition_static_beta(
        self, move_staff: callable, static_motions: List[MotionAttributesDicts]
    ) -> None:
        for arrow in static_motions:
            staff = next(
                (s for s in self.pictograph.props if s.arrow.color == arrow[COLOR]),
                None,
            )
            if not staff:
                continue

            end_location = arrow[END_LOCATION]
            layer_reposition_map = {
                1: {
                    (NORTH, RED): RIGHT,
                    (NORTH, BLUE): LEFT,
                    (SOUTH, RED): RIGHT,
                    (SOUTH, BLUE): LEFT,
                    (EAST, RED): (UP, DOWN) if end_location == EAST else None,
                    (WEST, BLUE): (UP, DOWN) if end_location == WEST else None,
                },
                2: {
                    (NORTH, RED): UP,
                    (NORTH, BLUE): DOWN,
                    (SOUTH, RED): UP,
                    (SOUTH, BLUE): DOWN,
                    (EAST, RED): (RIGHT, LEFT) if end_location == EAST else None,
                    (WEST, BLUE): (LEFT, RIGHT) if end_location == WEST else None,
                },
            }

            direction: Direction = layer_reposition_map[staff.layer].get(
                (staff.location, arrow[COLOR]), None
            )

            if direction:
                if isinstance(direction, str):
                    move_staff(staff, direction)
                elif isinstance(direction, tuple):
                    move_staff(staff, direction[0])
                    other_staff = next(
                        (
                            s
                            for s in self.pictograph.props
                            if s.location == staff.location and s != staff
                        ),
                        None,
                    )
                    if other_staff:
                        move_staff(other_staff, direction[1])

    ### ALPHA TO BETA ### D, E, F

    def reposition_alpha_to_beta(self, move_staff, converging_arrows) -> None:
        # check if all the staffs are in layer 1
        if all(staff.layer == 1 for staff in self.pictograph.props):
            end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
            start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
            if (
                end_locations[0] == end_locations[1]
                and start_locations[0] != start_locations[1]
            ):
                for arrow in converging_arrows:
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        move_staff(
                            next(
                                staff
                                for staff in self.pictograph.props
                                if staff.arrow.color == arrow[COLOR]
                            ),
                            direction,
                        )
        # check if all the staffs are in layer 2
        elif all(staff.layer == 2 for staff in self.pictograph.props):
            end_locations = [arrow[END_LOCATION] for arrow in converging_arrows]
            start_locations = [arrow[START_LOCATION] for arrow in converging_arrows]
            if (
                end_locations[0] == end_locations[1]
                and start_locations[0] != start_locations[1]
            ):
                for arrow in converging_arrows:
                    direction = self.determine_translation_direction(arrow)
                    if direction:
                        move_staff(
                            next(
                                staff
                                for staff in self.pictograph.props
                                if staff.arrow.color == arrow[COLOR]
                            ),
                            direction,
                        )
        # check if one staff is in layer 1 and the other is in layer 2
        elif any(staff.layer == 1 for staff in self.pictograph.props) and any(
            staff.layer == 2 for staff in self.pictograph.props
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
                        move_staff(
                            next(
                                staff
                                for staff in self.pictograph.props
                                if staff.arrow.color == arrow[COLOR]
                            ),
                            direction,
                        )

    ### BETA TO BETA ### G, H, I

    def reposition_beta_to_beta(self, motions) -> None:
        motion1, motion2 = motions
        same_motion_type = motion1[MOTION_TYPE] == motion2[MOTION_TYPE] in [PRO, ANTI]

        if all(staff.layer == 1 for staff in self.pictograph.props):
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

        further_staff = next(
            staff
            for staff in self.pictograph.props
            if staff.arrow.color == further_arrow[COLOR]
        )
        new_position_further = self.calculate_new_position(
            further_staff.pos(), further_direction
        )
        further_staff.setPos(new_position_further)

        other_direction = self.get_opposite_direction(further_direction)
        other_staff = next(
            staff
            for staff in self.pictograph.props
            if staff.arrow.color == other_arrow[COLOR]
        )
        new_position_other = self.calculate_new_position(
            other_staff.pos(), other_direction
        )
        other_staff.setPos(new_position_other)

    def reposition_I(self, motion1, motion2) -> None:
        pro_motion = motion1 if motion1[MOTION_TYPE] == PRO else motion2
        anti_motion = motion2 if motion1[MOTION_TYPE] == PRO else motion1

        pro_staff = next(
            (
                staff
                for staff in self.pictograph.props
                if staff.arrow.color == pro_motion[COLOR]
            ),
            None,
        )
        anti_staff = next(
            (
                staff
                for staff in self.pictograph.props
                if staff.arrow.color == anti_motion[COLOR]
            ),
            None,
        )

        if pro_staff and anti_staff:
            pro_staff_translation_direction = self.determine_translation_direction(
                pro_motion
            )
            anti_staff_translation_direction = self.get_opposite_direction(
                pro_staff_translation_direction
            )

            new_position_pro = self.calculate_new_position(
                pro_staff.pos(), pro_staff_translation_direction
            )
            pro_staff.setPos(new_position_pro)

            new_position_anti = self.calculate_new_position(
                anti_staff.pos(), anti_staff_translation_direction
            )
            anti_staff.setPos(new_position_anti)

    ### GAMMA TO BETA ### Y, Z

    def reposition_gamma_to_beta(self, move_staff, shifts, static_motions) -> None:
        shift, static_motion = shifts[0], static_motions[0]
        direction = self.determine_translation_direction(shift)
        if direction:
            move_staff(
                next(
                    staff
                    for staff in self.pictograph.props
                    if staff.arrow.color == shift[COLOR]
                ),
                direction,
            )
            move_staff(
                next(
                    staff
                    for staff in self.pictograph.props
                    if staff.arrow.color == static_motion[COLOR]
                ),
                self.get_opposite_direction(direction),
            )

    ### HELPERS ###

    def staffs_in_beta(self) -> bool | None:
        visible_staves: List[Staff] = []
        for staff in self.pictograph.props:
            if staff.isVisible():
                visible_staves.append(staff)
        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                return True
            else:
                return False

    def find_optimal_arrow_location_entry(
        self,
        current_state,
        matching_letters,
        arrow_dict,
    ) -> OptimalLocationEntries | None:
        for variants in matching_letters:
            if self.pictograph.arrow_positioner.compare_states(current_state, variants):
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
        if motion[END_LAYER] == 1:
            if motion[MOTION_TYPE] in [PRO, ANTI, STATIC]:
                if motion[END_LOCATION] in [NORTH, SOUTH]:
                    return RIGHT if motion[START_LOCATION] == EAST else LEFT
                elif motion[END_LOCATION] in [EAST, WEST]:
                    return DOWN if motion[START_LOCATION] == SOUTH else UP
        elif motion[END_LAYER] == 2:
            if motion[MOTION_TYPE] in [PRO, ANTI, STATIC]:
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
        else:
            return current_position - offset

    ### GETTERS

    def get_distance_from_center(self, arrow_pos: Dict[str, float]) -> float:
        grid_center = self.pictograph.grid.center
        arrow_x, arrow_y = arrow_pos.get("x", 0.0), arrow_pos.get("y", 0.0)
        center_x, center_y = grid_center.x(), grid_center.y()

        distance_from_center = math.sqrt(
            (arrow_x - center_x) ** 2 + (arrow_y - center_y) ** 2
        )
        return distance_from_center

    def get_optimal_arrow_location(
        self, arrow_attributes: ArrowAttributesDicts
    ) -> Dict[str, float] | None:
        current_state = self.pictograph.get_state()
        current_letter = self.pictograph.current_letter

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