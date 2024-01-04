from email.charset import QP
from PyQt6.QtCore import QPointF
from Enums import Letter, LetterNumberType
from constants import *
from objects.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Union


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.Type1_arrow_positioner import (
        Type1ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type2_arrow_positioner import (
        Type2ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type3_arrow_positioner import (
        Type3ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type4_arrow_positioner import (
        Type4ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type5_arrow_positioner import (
        Type5ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.Type6_arrow_positioner import (
        Type6ArrowPositioner,
    )


class BaseArrowPositioner:
    ### SETUP ###
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.arrows = pictograph.arrows.values()
        self.ghost_arrows = pictograph.ghost_arrows.values()
        self.letters: Dict[
            Letter, List[Dict[str, str]]
        ] = pictograph.main_widget.letters
        self.letters_to_reposition: List[Letter] = ["G", "H", "I", "P", "Q", "R", "Λ-"]

    ### PUBLIC METHODS ###
    def update_arrow_positions(self) -> None:
        self.ghost_arrows = self.pictograph.ghost_arrows.values()
        self.letter = self.pictograph.letter
        self.letter_type = self.get_letter_type(self.letter)

        for arrow in self.pictograph.arrows.values():
            if arrow.motion.is_shift():
                self._set_shift_to_default_coor(arrow)
                self._set_shift_to_default_coor(arrow.ghost)
            elif arrow.motion.is_dash():
                self._set_dash_to_default_coor(arrow)
                self._set_dash_to_default_coor(arrow.ghost)

        if self.letter in self.letters_to_reposition:
            self._reposition_arrows()

    def _reposition_arrows(
        self: Union[
            "Type1ArrowPositioner",
            "Type2ArrowPositioner",
            "Type3ArrowPositioner",
            "Type4ArrowPositioner",
            "Type5ArrowPositioner",
            "Type6ArrowPositioner",
        ]
    ) -> None:
        if self.letter_type == "Type1":
            reposition_methods = {
                "G": self._reposition_G_H,
                "H": self._reposition_G_H,
                "I": self._reposition_I,
                "P": self._reposition_P,
                "Q": self._reposition_Q,
                "R": self._reposition_R,
            }
        elif self.letter_type == "Type5":
            reposition_methods = {
                "Λ-": self._reposition_Λ_dash,
            }

        reposition_method = reposition_methods.get(self.letter)
        if reposition_method:
            reposition_method()

    ### SHIFT ###
    def _set_shift_to_default_coor(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        default_pos = self._get_default_shift_coord(arrow)
        adjustment = self.calculate_shift_adjustment(arrow)
        new_pos = default_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)

    ### DASH ###
    def _set_dash_to_default_coor(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        default_red_pos = self._get_default_dash_coord(arrow.scene.arrows[RED])
        default_blue_pos = self._get_default_dash_coord(arrow.scene.arrows[BLUE])
        red_adjustment, blue_adjustment = self.calculate_dash_adjustments(arrow)
        new_red_pos = default_red_pos + red_adjustment - arrow.boundingRect().center()
        new_blue_pos = (
            default_blue_pos + blue_adjustment - arrow.boundingRect().center()
        )
        arrow.scene.arrows[RED].setPos(new_red_pos)
        arrow.scene.arrows[BLUE].setPos(new_blue_pos)

    ### GETTERS ###
    def _get_default_shift_coord(self, arrow: Arrow) -> QPointF:
        layer2_points = self.pictograph.grid.get_layer2_points()
        return layer2_points.get(arrow.loc, QPointF(0, 0))

    def _get_default_dash_coord(self, arrow: Arrow) -> QPointF:
        handpoints = self.pictograph.grid.get_handpoints()
        other_arrow = (
            self.pictograph.arrows[RED]
            if arrow.color == BLUE
            else self.pictograph.arrows[BLUE]
        )
        if arrow.turns == 0:
            if other_arrow.motion.is_shift():
                if arrow.motion.end_loc in [NORTH, SOUTH]:
                    if other_arrow.loc in [SOUTHEAST, NORTHEAST]:
                        return handpoints.get(WEST)
                    elif other_arrow.loc in [SOUTHWEST, NORTHWEST]:
                        return handpoints.get(EAST)
                elif arrow.motion.end_loc in [EAST, WEST]:
                    if other_arrow.loc in [SOUTHEAST, SOUTHWEST]:
                        return handpoints.get(NORTH)
                    elif other_arrow.loc in [NORTHEAST, NORTHWEST]:
                        return handpoints.get(SOUTH)
                else:
                    print("ERROR: Arrow motion end_loc not found")
            elif other_arrow.motion.is_dash():
                if other_arrow.loc == arrow.loc and arrow.loc is not None:
                    opposite_location = self.get_opposite_location(arrow.loc)
                    arrow.loc = opposite_location
                    return handpoints.get(opposite_location)
                elif other_arrow.loc == self.get_opposite_location(arrow.loc):
                    if arrow.motion.end_loc in [NORTH, SOUTH]:
                        if other_arrow.loc == WEST:
                            return handpoints.get(EAST)
                        elif other_arrow.loc == EAST:
                            return handpoints.get(WEST)
                    elif arrow.motion.end_loc in [EAST, WEST]:
                        if other_arrow.loc == NORTH:
                            return handpoints.get(SOUTH)
                        elif other_arrow.loc == SOUTH:
                            return handpoints.get(NORTH)
                elif self.pictograph.letter == "Λ-":
                    dir_map = {
                        ((NORTH, SOUTH), (EAST, WEST)): EAST,
                        ((EAST, WEST), (NORTH, SOUTH)): NORTH,
                        ((NORTH, SOUTH), (WEST, EAST)): WEST,
                        ((WEST, EAST), (NORTH, SOUTH)): NORTH,
                        ((SOUTH, NORTH), (EAST, WEST)): EAST,
                        ((EAST, WEST), (SOUTH, NORTH)): SOUTH,
                        ((SOUTH, NORTH), (WEST, EAST)): WEST,
                        ((WEST, EAST), (SOUTH, NORTH)): SOUTH,
                    }

                    arrow_loc = dir_map.get(
                        (
                            (arrow.motion.start_loc, arrow.motion.end_loc),
                            (other_arrow.motion.start_loc, other_arrow.motion.end_loc),
                        )
                    )

                    arrow.loc = arrow_loc
                    return handpoints.get(arrow_loc)

            elif other_arrow.motion.is_static():
                return handpoints.get(arrow.loc)
            else:
                print("ERROR: Arrow motion not found")
        elif arrow.turns > 0:
            if arrow.motion.prop_rot_dir == CLOCKWISE:
                if arrow.motion.start_loc == NORTH:
                    if arrow.motion.end_loc == SOUTH:
                        return handpoints.get(EAST)
                elif arrow.motion.start_loc == EAST:
                    if arrow.motion.end_loc == WEST:
                        return handpoints.get(SOUTH)
                elif arrow.motion.start_loc == SOUTH:
                    if arrow.motion.end_loc == NORTH:
                        return handpoints.get(WEST)
                elif arrow.motion.start_loc == WEST:
                    if arrow.motion.end_loc == EAST:
                        return handpoints.get(NORTH)
            elif arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                if arrow.motion.start_loc == NORTH:
                    if arrow.motion.end_loc == SOUTH:
                        return handpoints.get(WEST)
                elif arrow.motion.start_loc == EAST:
                    if arrow.motion.end_loc == WEST:
                        return handpoints.get(NORTH)
                elif arrow.motion.start_loc == SOUTH:
                    if arrow.motion.end_loc == NORTH:
                        return handpoints.get(EAST)
                elif arrow.motion.start_loc == WEST:
                    if arrow.motion.end_loc == EAST:
                        return handpoints.get(SOUTH)

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_map.get(location, "")

    def _calculate_adjustment_tuple(self, location: str, distance: int) -> QPointF:
        location_adjustments = {
            NORTHEAST: QPointF(distance, -distance),
            SOUTHEAST: QPointF(distance, distance),
            SOUTHWEST: QPointF(-distance, distance),
            NORTHWEST: QPointF(-distance, -distance),
        }
        return location_adjustments.get(location, QPointF(0, 0))

    def are_adjacent_locations(self, location1: str, location2: str) -> bool:
        adjacent_map = {
            NORTHEAST: [NORTH, EAST],
            SOUTHEAST: [SOUTH, EAST],
            SOUTHWEST: [SOUTH, WEST],
            NORTHWEST: [NORTH, WEST],
        }
        return location2 in adjacent_map.get(location1, [])

    ### HELPERS ###
    def _is_arrow_movable(self, arrow: Arrow) -> bool:
        return (
            not arrow.is_dragging
            and arrow.motion
            and arrow.motion.motion_type != STATIC
        )

    def compare_states(self, current_state: Dict, candidate_state: Dict) -> bool:
        relevant_keys = [
            LETTER,
            START_POS,
            END_POS,
            BLUE_MOTION_TYPE,
            BLUE_PROP_ROT_DIR,
            BLUE_TURNS,
            BLUE_START_LOC,
            BLUE_END_LOC,
            RED_MOTION_TYPE,
            RED_PROP_ROT_DIR,
            RED_TURNS,
            RED_START_LOC,
            RED_END_LOC,
        ]
        return all(
            current_state.get(key) == candidate_state.get(key) for key in relevant_keys
        )

    def calculate_shift_adjustment(self, arrow: Arrow) -> QPointF:
        if arrow.motion_type == PRO:
            location_adjustments = {
                (0, CLOCKWISE): {
                    NORTHEAST: QPointF(40, -35),
                    SOUTHEAST: QPointF(35, 40),
                    SOUTHWEST: QPointF(-40, 35),
                    NORTHWEST: QPointF(-35, -40),
                },
                (0, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(35, -40),
                    SOUTHEAST: QPointF(40, 35),
                    SOUTHWEST: QPointF(-35, 40),
                    NORTHWEST: QPointF(-40, -35),
                },
                (0.5, CLOCKWISE): {
                    NORTHEAST: QPointF(0, 50),
                    SOUTHEAST: QPointF(-50, 0),
                    SOUTHWEST: QPointF(0, -50),
                    NORTHWEST: QPointF(50, 0),
                },
                (0.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(-50, 0),
                    SOUTHEAST: QPointF(0, -50),
                    SOUTHWEST: QPointF(50, 0),
                    NORTHWEST: QPointF(0, 50),
                },
                (1, CLOCKWISE): {
                    NORTHEAST: QPointF(-25, -15),
                    SOUTHEAST: QPointF(15, -25),
                    SOUTHWEST: QPointF(25, 15),
                    NORTHWEST: QPointF(-15, 25),
                },
                (1, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(15, 25),
                    SOUTHEAST: QPointF(-25, 15),
                    SOUTHWEST: QPointF(-15, -25),
                    NORTHWEST: QPointF(25, -15),
                },
                (1.5, CLOCKWISE): {
                    NORTHEAST: QPointF(0, 20),
                    SOUTHEAST: QPointF(-20, 0),
                    SOUTHWEST: QPointF(0, -20),
                    NORTHWEST: QPointF(20, 0),
                },
                (1.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(-20, 0),
                    SOUTHEAST: QPointF(0, -20),
                    SOUTHWEST: QPointF(20, 0),
                    NORTHWEST: QPointF(0, 20),
                },
                (2, CLOCKWISE): {
                    NORTHEAST: QPointF(40, -35),
                    SOUTHEAST: QPointF(35, 40),
                    SOUTHWEST: QPointF(-40, 35),
                    NORTHWEST: QPointF(-35, -40),
                },
                (2, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(35, -40),
                    SOUTHEAST: QPointF(40, 35),
                    SOUTHWEST: QPointF(-35, 40),
                    NORTHWEST: QPointF(-40, -35),
                },
                (2.5, CLOCKWISE): {
                    NORTHEAST: QPointF(0, 35),
                    SOUTHEAST: QPointF(-35, 0),
                    SOUTHWEST: QPointF(0, -35),
                    NORTHWEST: QPointF(35, 0),
                },
                (2.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(-35, 0),
                    SOUTHEAST: QPointF(0, -35),
                    SOUTHWEST: QPointF(35, 0),
                    NORTHWEST: QPointF(0, 35),
                },
                (3, CLOCKWISE): {
                    NORTHEAST: QPointF(-25, -15),
                    SOUTHEAST: QPointF(15, -25),
                    SOUTHWEST: QPointF(25, 15),
                    NORTHWEST: QPointF(-15, 25),
                },
                (3, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(15, 25),
                    SOUTHEAST: QPointF(-25, 15),
                    SOUTHWEST: QPointF(-15, -25),
                    NORTHWEST: QPointF(25, -15),
                },
            }
        elif arrow.motion_type == ANTI:
            location_adjustments = {
                (0, CLOCKWISE): {
                    NORTHEAST: QPointF(40, -35),
                    SOUTHEAST: QPointF(35, 40),
                    SOUTHWEST: QPointF(-40, 35),
                    NORTHWEST: QPointF(-35, -40),
                },
                (0, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(35, -40),
                    SOUTHEAST: QPointF(40, 35),
                    SOUTHWEST: QPointF(-35, 40),
                    NORTHWEST: QPointF(-40, -35),
                },
                (0.5, CLOCKWISE): {
                    NORTHEAST: QPointF(-80, 95),
                    SOUTHEAST: QPointF(-95, -80),
                    SOUTHWEST: QPointF(80, -95),
                    NORTHWEST: QPointF(95, 80),
                },
                (0.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(-95, 80),
                    SOUTHEAST: QPointF(-80, -95),
                    SOUTHWEST: QPointF(95, -80),
                    NORTHWEST: QPointF(80, 95),
                },
                (1, CLOCKWISE): {
                    NORTHEAST: QPointF(20, -25),
                    SOUTHEAST: QPointF(25, 20),
                    SOUTHWEST: QPointF(-20, 25),
                    NORTHWEST: QPointF(-25, -20),
                },
                (1, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(25, -20),
                    SOUTHEAST: QPointF(20, 25),
                    SOUTHWEST: QPointF(-25, 20),
                    NORTHWEST: QPointF(-20, -25),
                },
                (1.5, CLOCKWISE): {
                    NORTHEAST: QPointF(-55, -10),
                    SOUTHEAST: QPointF(10, -55),
                    SOUTHWEST: QPointF(55, 10),
                    NORTHWEST: QPointF(-10, 55),
                },
                (1.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(10, 55),
                    SOUTHEAST: QPointF(-55, 10),
                    SOUTHWEST: QPointF(-10, -55),
                    NORTHWEST: QPointF(55, -10),
                },
                (2, CLOCKWISE): {
                    NORTHEAST: QPointF(40, -35),
                    SOUTHEAST: QPointF(35, 40),
                    SOUTHWEST: QPointF(-40, 35),
                    NORTHWEST: QPointF(-35, -40),
                },
                (2, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(35, -40),
                    SOUTHEAST: QPointF(40, 35),
                    SOUTHWEST: QPointF(-35, 40),
                    NORTHWEST: QPointF(-40, -35),
                },
                (2.5, CLOCKWISE): {
                    NORTHEAST: QPointF(-60, 95),
                    SOUTHEAST: QPointF(-95, -60),
                    SOUTHWEST: QPointF(60, -95),
                    NORTHWEST: QPointF(95, 60),
                },
                (2.5, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(-95, 60),
                    SOUTHEAST: QPointF(-60, -95),
                    SOUTHWEST: QPointF(95, -60),
                    NORTHWEST: QPointF(60, 95),
                },
                (3, CLOCKWISE): {
                    NORTHEAST: QPointF(20, -25),
                    SOUTHEAST: QPointF(25, 20),
                    SOUTHWEST: QPointF(-20, 25),
                    NORTHWEST: QPointF(-25, -20),
                },
                (3, COUNTER_CLOCKWISE): {
                    NORTHEAST: QPointF(25, -20),
                    SOUTHEAST: QPointF(20, 25),
                    SOUTHWEST: QPointF(-25, 20),
                    NORTHWEST: QPointF(-20, -25),
                },
            }
        return location_adjustments.get(
            (arrow.turns, arrow.motion.prop_rot_dir), {}
        ).get(arrow.loc)

    def calculate_dash_adjustments(self, arrow: Arrow) -> QPointF:
        if arrow.motion.prop_rot_dir == CLOCKWISE:
            if arrow.loc == WEST:
                red_adjustment = QPointF(-80, 0)
                blue_adjustment = QPointF(-10, 0)
            elif arrow.loc == EAST:
                red_adjustment = QPointF(50, 0)
                blue_adjustment = QPointF(-25, 0)
            elif arrow.loc == NORTH:
                red_adjustment = QPointF(0, -80)
                blue_adjustment = QPointF(0, -10)
            elif arrow.loc == SOUTH:
                red_adjustment = QPointF(0, 50)
                blue_adjustment = QPointF(0, -25)
                
        elif arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            if arrow.loc == WEST:
                red_adjustment = QPointF(-80, 0)
                blue_adjustment = QPointF(-10, 0)
            elif arrow.loc == EAST:
                red_adjustment = QPointF(-80, 0)
                blue_adjustment = QPointF(-10, 0)
            elif arrow.loc == NORTH:
                red_adjustment = QPointF(0, 80)
                blue_adjustment = QPointF(0, 10)
            elif arrow.loc == SOUTH:
                red_adjustment = QPointF(0, 80)
                blue_adjustment = QPointF(0, 10)
        elif arrow.motion.prop_rot_dir == NO_ROT:
            red_adjustment = QPointF(0, 0)
            blue_adjustment = QPointF(0, 0)

        return red_adjustment, blue_adjustment

    def _apply_shift_adjustment(
        self, arrow: Arrow, adjustment: QPointF, update_ghost: bool = True
    ) -> None:
        default_pos = self._get_default_shift_coord(arrow)
        arrow_center = arrow.boundingRect().center()
        new_pos = default_pos - arrow_center + adjustment
        arrow.setPos(new_pos)

        # Update the ghost arrow with the same adjustment
        if update_ghost and arrow.ghost:
            self._apply_shift_adjustment(arrow.ghost, adjustment, update_ghost=False)

    def _apply_dash_adjustment(
        self, arrow: Arrow, adjustment: QPointF, update_ghost: bool = True
    ) -> None:
        default_pos = self._get_default_dash_coord(arrow)
        arrow_center = arrow.boundingRect().center()
        new_pos = default_pos - arrow_center + adjustment
        arrow.setPos(new_pos)

        # Update the ghost arrow with the same adjustment
        if update_ghost and arrow.ghost:
            self._apply_dash_adjustment(arrow.ghost, adjustment, update_ghost=False)

    # Function to get the Enum member key from a given letter
    def get_letter_type(self, letter: str) -> str | None:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return (
                    letter_type.name.replace("_", "").lower().capitalize()
                )  # Modify the key format
        return None
