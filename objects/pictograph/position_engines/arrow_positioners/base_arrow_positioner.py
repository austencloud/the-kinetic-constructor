from PyQt6.QtCore import QPointF
from Enums import Letter
from constants import *
from objects.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Union


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type1_arrow_positioner import (
        Type1ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type2_arrow_positioner import (
        Type2ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type3_arrow_positioner import (
        Type3ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type4_arrow_positioner import (
        Type4ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type5_arrow_positioner import (
        Type5ArrowPositioner,
    )
    from objects.pictograph.position_engines.arrow_positioners.by_motion_type.Type6_arrow_positioner import (
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
        self.letters_to_reposition: List[Letter] = ["G", "H", "I", "P", "Q", "R"]

    ### PUBLIC METHODS ###
    def update_arrow_positions(self) -> None:
        self.ghost_arrows = self.pictograph.ghost_arrows.values()
        self.current_letter = self.pictograph.letter

        for arrow in self.pictograph.arrows.values():
            if arrow.motion.is_shift():
                self._set_shift_to_default_loc(arrow)
                self._set_shift_to_default_loc(arrow.ghost)
            elif arrow.motion.is_dash():
                self._set_dash_to_default_loc(arrow)
                self._set_dash_to_default_loc(arrow.ghost)

        if self.current_letter in self.letters_to_reposition:
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
        reposition_methods = {
            "G": self._reposition_G_H,
            "H": self._reposition_G_H,
            "I": self._reposition_I,
            "P": self._reposition_P,
            "Q": self._reposition_Q,
            "R": self._reposition_R,
        }

        reposition_method = reposition_methods.get(self.current_letter)
        if reposition_method:
            reposition_method()

    ### SHIFT ###
    def _set_shift_to_default_loc(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        if not arrow.is_ghost:
            arrow.ghost.set_arrow_transform_origin_to_center()
        default_pos = self._get_default_shift_loc(arrow)
        adjustment = self.calculate_adjustment(arrow.location, DISTANCE)
        new_pos = default_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)

    ### DASH ###
    def _set_dash_to_default_loc(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        if not arrow.is_ghost:
            arrow.ghost.set_arrow_transform_origin_to_center()
        default_pos = self._get_default_dash_loc(arrow)
        adjustment = self.calculate_adjustment(arrow.location, DISTANCE)
        new_pos = default_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)

    ### GETTERS ###
    def _get_default_shift_loc(self, arrow: Arrow) -> QPointF:
        layer2_points = self.pictograph.grid.get_layer2_points()
        return layer2_points.get(arrow.location, QPointF(0, 0))

    def _get_default_dash_loc(self, arrow: Arrow) -> QPointF:
        handpoints = self.pictograph.grid.get_handpoints()
        other_arrow = (
            self.pictograph.arrows[RED]
            if arrow.color == BLUE
            else self.pictograph.arrows[BLUE]
        )
        if other_arrow.motion.is_shift():
            if arrow.motion.end_loc in [NORTH, SOUTH]:
                if other_arrow.location in [SOUTHEAST, NORTHEAST]:
                    return handpoints.get(WEST)
                elif other_arrow.location in [SOUTHWEST, NORTHWEST]:
                    return handpoints.get(EAST)
            elif arrow.motion.end_loc in [EAST, WEST]:
                if other_arrow.location in [SOUTHEAST, SOUTHWEST]:
                    return handpoints.get(NORTH)
                elif other_arrow.location in [NORTHEAST, NORTHWEST]:
                    return handpoints.get(SOUTH)
            else:
                print("ERROR: Arrow motion end_loc not found")
        elif other_arrow.motion.is_dash():
            if other_arrow.location == arrow.location:
                opposite_location = self.get_opposite_location(arrow.location)
                arrow.location = opposite_location
                return handpoints.get(opposite_location)
            elif other_arrow.location == self.get_opposite_location(arrow.location):
                if arrow.motion.end_loc in [NORTH, SOUTH]:
                    if other_arrow.location == WEST:
                        return handpoints.get(EAST)
                    elif other_arrow.location == EAST:
                        return handpoints.get(WEST)
                elif arrow.motion.end_loc in [EAST, WEST]:
                    if other_arrow.location == NORTH:
                        return handpoints.get(SOUTH)
                    elif other_arrow.location == SOUTH:
                        return handpoints.get(NORTH)                
            else:
                return handpoints.get(arrow.location)

        elif other_arrow.motion.is_static():
            return handpoints.get(arrow.location)
        else:
            print("ERROR: Arrow motion not found")

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
            "blue_turns",
            BLUE_START_LOC,
            BLUE_END_LOC,
            RED_MOTION_TYPE,
            RED_PROP_ROT_DIR,
            "red_turns",
            RED_START_LOC,
            RED_END_LOC,
        ]
        return all(
            current_state.get(key) == candidate_state.get(key) for key in relevant_keys
        )

    ### UNIVERSAL METHODS ###
    def calculate_adjustment(self, location: str, distance: int) -> QPointF:
        location_adjustments = {
            NORTHEAST: QPointF(distance, -distance),
            SOUTHEAST: QPointF(distance, distance),
            SOUTHWEST: QPointF(-distance, distance),
            NORTHWEST: QPointF(-distance, -distance),
        }
        return location_adjustments.get(location, QPointF(0, 0))

    def _apply_adjustment(
        self, arrow: Arrow, adjustment: QPointF, update_ghost: bool = True
    ) -> None:
        default_pos = self._get_default_shift_loc(arrow)
        arrow_center = arrow.boundingRect().center()
        new_pos = default_pos - arrow_center + adjustment
        arrow.setPos(new_pos)

        # Update the ghost arrow with the same adjustment
        if update_ghost and arrow.ghost:
            self._apply_adjustment(arrow.ghost, adjustment, update_ghost=False)
