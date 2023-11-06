from PyQt6.QtCore import QPointF
import math
from settings.numerical_constants import (
    GRAPHBOARD_VIEW_WIDTH,
    GRAPHBOARD_SCALE,
    PICTOGRAPH_SCALE,
    BETA_OFFSET,
)
from settings.string_constants import *


class StaffPositioner:
    def __init__(self, staff, scene):
        self.staff = staff
        self.scene = scene
        self.letters = staff.scene.main_widget.letters

    ### REPOSITIONERS ###

    def check_replace_beta_staffs(self, scene):
        board_state = scene.get_state()

        visible_staves = []

        for staff in scene.staffs:
            if staff.isVisible():
                visible_staves.append(staff)

        if len(visible_staves) == 2:
            if visible_staves[0].location == visible_staves[1].location:
                self.reposition_staffs(scene, board_state)

    def reposition_staffs(self, scene, board_state):
        def move_staff(staff, direction):
            new_position = self.calculate_new_position(staff.pos(), direction)
            staff.setPos(new_position)

        arrows_grouped_by_start = {}
        for arrow in board_state[ARROWS]:
            arrows_grouped_by_start.setdefault(arrow[START_LOCATION], []).append(arrow)

        pro_or_anti_arrows = [
            arrow for arrow in board_state[ARROWS] if arrow[MOTION_TYPE] in [PRO, ANTI]
        ]
        static_arrows = [
            arrow for arrow in board_state[ARROWS] if arrow[MOTION_TYPE] == STATIC
        ]

        # STATIC BETA
        if len(static_arrows) > 1:
            self.reposition_static_beta(move_staff, static_arrows)

        # BETA → BETA - G, H, I
        for start_location, arrows in arrows_grouped_by_start.items():
            if len(arrows) == 2:
                arrow1, arrow2 = arrows
                if (
                    arrow1[START_LOCATION] == arrow2[START_LOCATION]
                    and arrow1[END_LOCATION] == arrow2[END_LOCATION]
                ):
                    if arrow1[MOTION_TYPE] in [PRO, ANTI] and arrow2[MOTION_TYPE] in [
                        PRO,
                        ANTI,
                    ]:
                        self.reposition_beta_to_beta(scene, arrows)

        # GAMMA → BETA - Y, Z
        if len(pro_or_anti_arrows) == 1 and len(static_arrows) == 1:
            self.reposition_gamma_to_beta(move_staff, pro_or_anti_arrows, static_arrows)

        # ALPHA → BETA - D, E, F
        converging_arrows = [
            arrow for arrow in board_state[ARROWS] if arrow[MOTION_TYPE] not in [STATIC]
        ]
        if len(converging_arrows) == 2:
            if converging_arrows[0].get(START_LOCATION) != converging_arrows[1].get(
                START_LOCATION
            ):
                self.reposition_alpha_to_beta(move_staff, converging_arrows)

        scene.update()

    def reposition_static_beta(self, move_staff, static_arrows, scale):
        for arrow in static_arrows:
            staff = next(
                (
                    staff
                    for staff in self.scene.staffs
                    if staff.arrow.color == arrow[COLOR]
                ),
                None,
            )
            if not staff:
                continue

            end_location = arrow.get(END_LOCATION, "")

            beta_reposition_map = {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): (UP, DOWN) if end_location == EAST else None,
                (WEST, BLUE): (UP, DOWN) if end_location == WEST else None,
            }

            direction = beta_reposition_map.get((staff.location, arrow[COLOR]), None)

            if direction:
                if isinstance(direction, str):
                    move_staff(staff, direction)
                elif isinstance(direction, tuple):
                    move_staff(staff, direction[0])
                    other_staff = next(
                        (
                            s
                            for s in self.scene.staffs
                            if s.location == staff.location and s != staff
                        ),
                        None,
                    )
                    if other_staff:
                        move_staff(other_staff, direction[1])

    def reposition_alpha_to_beta(self, move_staff, converging_arrows):  # D, E, F
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
                            for staff in self.scene.staffs
                            if staff.arrow.color == arrow[COLOR]
                        ),
                        direction,
                    )

    def reposition_beta_to_beta(self, scene, arrows):  # G, H, I
        if len(arrows) != 2:
            return

        arrow1, arrow2 = arrows
        same_motion_type = arrow1[MOTION_TYPE] == arrow2[MOTION_TYPE] in [PRO, ANTI]

        if same_motion_type:
            self.reposition_G_and_H(scene, arrow1, arrow2)

        else:
            self.reposition_I(arrow1, arrow2)

        scene.update()

    def reposition_G_and_H(self, scene, arrow1, arrow2):
        optimal_position1 = self.get_optimal_arrow_location(arrow1, scene)
        optimal_position2 = self.get_optimal_arrow_location(arrow2, scene)

        if not optimal_position1 or not optimal_position2:
            return

        distance1 = self.get_distance_from_center(optimal_position1)
        distance2 = self.get_distance_from_center(optimal_position2)

        further_arrow = arrow1 if distance1 > distance2 else arrow2
        other_arrow = arrow1 if further_arrow == arrow2 else arrow2

        further_direction = self.determine_translation_direction(further_arrow)

        further_staff = next(
            staff
            for staff in self.scene.staffs
            if staff.arrow.color == further_arrow[COLOR]
        )
        new_position_further = self.calculate_new_position(
            further_staff.pos(), further_direction
        )
        further_staff.setPos(new_position_further)

        other_direction = self.get_opposite_direction(further_direction)
        other_staff = next(
            staff
            for staff in self.scene.staffs
            if staff.arrow.color == other_arrow[COLOR]
        )
        new_position_other = self.calculate_new_position(
            other_staff.pos(), other_direction
        )
        other_staff.setPos(new_position_other)

    def reposition_I(self, arrow1, arrow2):
        pro_arrow = arrow1 if arrow1[MOTION_TYPE] == PRO else arrow2
        anti_arrow = arrow2 if arrow1[MOTION_TYPE] == PRO else arrow1

        pro_staff = next(
            (
                staff
                for staff in self.scene.staffs
                if staff.arrow.color == pro_arrow[COLOR]
            ),
            None,
        )
        anti_staff = next(
            (
                staff
                for staff in self.scene.staffs
                if staff.arrow.color == anti_arrow[COLOR]
            ),
            None,
        )

        if pro_staff and anti_staff:
            pro_staff_translation_direction = self.determine_translation_direction(
                pro_arrow
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

    def reposition_gamma_to_beta(
        self, move_staff, pro_or_anti_arrows, static_arrows
    ):  # Y, Z
        pro_or_anti_arrow, static_arrow = pro_or_anti_arrows[0], static_arrows[0]
        direction = self.determine_translation_direction(pro_or_anti_arrow)
        if direction:
            move_staff(
                next(
                    staff
                    for staff in self.scene.staffs
                    if staff.arrow.color == pro_or_anti_arrow[COLOR]
                ),
                direction,
            )
            move_staff(
                next(
                    staff
                    for staff in self.scene.staffs
                    if staff.arrow.color == static_arrow[COLOR]
                ),
                self.get_opposite_direction(direction),
            )

    ### HELPERS ###

    def get_distance_from_center(self, position):
        center_point = QPointF(
            GRAPHBOARD_VIEW_WIDTH / 2, GRAPHBOARD_VIEW_WIDTH / 2
        )  # Assuming this is the center point of your coordinate system

        x_position = position.get("x", 0.0)
        y_position = position.get("y", 0.0)
        center_x = center_point.x()
        center_y = center_point.y()

        # Calculate the distance
        distance = math.sqrt(
            (x_position - center_x) ** 2 + (y_position - center_y) ** 2
        )
        return distance

    def get_optimal_arrow_location(self, arrow, scene):
        current_state = scene.get_state()
        current_letter = scene.info_handler.determine_current_letter_and_type()[0]

        if current_letter is not None:
            matching_letters = self.letters[current_letter]
            optimal_location = self.find_optimal_arrow_location(
                current_state, scene, matching_letters, arrow
            )

            if optimal_location:
                return optimal_location

        return None  # Return None if there are no optimal positions

    def find_optimal_arrow_location(
        self, current_state, scene, matching_letters, arrow_dict
    ):
        for variations in matching_letters:
            if scene.main_widget.arrow_manager.state_comparator.compare_states(
                current_state, variations
            ):
                optimal_entry = next(
                    (
                        d
                        for d in variations
                        if "optimal_red_location" in d and "optimal_blue_location" in d
                    ),
                    None,
                )

                if optimal_entry:
                    color_key = f"optimal_{arrow_dict['color']}_location"
                    return optimal_entry.get(color_key)

        return None

    def determine_translation_direction(self, arrow_state):
        """Determine the translation direction based on the arrow's board_state."""
        if arrow_state[MOTION_TYPE] in [PRO, ANTI]:
            if arrow_state[END_LOCATION] in [NORTH, SOUTH]:
                return RIGHT if arrow_state[START_LOCATION] == EAST else LEFT
            elif arrow_state[END_LOCATION] in [EAST, WEST]:
                return DOWN if arrow_state[START_LOCATION] == SOUTH else UP
        return None

    def calculate_new_position(self, current_position, direction):
        """Calculate the new position based on the direction."""
        offset = (
            QPointF(BETA_OFFSET, 0)
            if direction in [LEFT, RIGHT]
            else QPointF(0, BETA_OFFSET)
        )
        if direction in [RIGHT, DOWN]:
            return current_position + offset
        else:
            return current_position - offset

    def get_opposite_direction(self, movement):
        if movement == LEFT:
            return RIGHT
        elif movement == RIGHT:
            return LEFT
        elif movement == UP:
            return DOWN
        elif movement == DOWN:
            return UP

    ### UPDATERS ###

    def update_staff_position_based_on_quadrant(self, staff, quadrant):
        new_position = self.calculate_new_position_based_on_quadrant(staff, quadrant)
        staff.setPos(new_position)
