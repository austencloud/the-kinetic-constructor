from PyQt6.QtCore import QPointF
import pandas as pd
from Enums import Color, Location, MotionType, Orientation, PropType, RotationDirection
from constants.string_constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Callable
from objects.pictograph.position_engines.arrow_positioners.staff_arrow_positioner import (
    StaffArrowPositioner,
)
from objects.pictograph.position_engines.arrow_positioners.triad_arrow_positioner import (
    TriadArrowPositioner,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


DISTANCE = 40


class ArrowPositioner:
    ### SETUP ###
    def __init__(self, pictograph: "Pictograph") -> None:
        self.letters = pictograph.main_widget.letters
        self.pictograph = pictograph
        self.triad_arrow_positioner = TriadArrowPositioner(pictograph, self)
        self.staff_arrow_positioner = StaffArrowPositioner(pictograph, self)

    ### PUBLIC METHODS ###
    def update_arrow_positions(self) -> None:
        current_letter = self.pictograph.current_letter
        state_dict = self.pictograph.get_state()

        for arrow in self.pictograph.arrows.values():
            arrow.set_arrow_transform_origin_to_center()

        self._apply_default_positioning(current_letter, state_dict)

    ### POSITIONING LOGIC ###
    def _apply_default_positioning(self, current_letter, state_dict):
        reposition_method = self._get_reposition_method(current_letter)
        reposition_method()

        if self.pictograph.main_widget.prop_type == TRIAD:
            self.triad_arrow_positioner._adjust_arrows_for_triads(current_letter)
        elif self.pictograph.main_widget.prop_type == STAFF:
            self.staff_arrow_positioner._adjust_arrows_for_staffs(current_letter)

    def _calculate_adjustment_tuple(self, location: str, distance: int) -> QPointF:
        location_adjustments = {
            NORTHEAST: QPointF(distance, -distance),
            SOUTHEAST: QPointF(distance, distance),
            SOUTHWEST: QPointF(-distance, distance),
            NORTHWEST: QPointF(-distance, -distance),
        }
        return location_adjustments.get(location, QPointF(0, 0))

    def _get_reposition_method(self, current_letter) -> Callable:
        positioning_methods = {
            "G": self._reposition_GH,
            "H": self._reposition_GH,
            "I": self._reposition_I,
            "P": self._reposition_P,
            "Q": self._reposition_Q,
            "R": self._reposition_R,
        }
        return positioning_methods.get(
            current_letter, self._reposition_to_default_locations
        )

    def _reposition_to_default_locations(self) -> None:
        for arrow in self.pictograph.arrows.values():
            if self._is_arrow_movable(arrow):
                self._reposition_to_default_loc(arrow)
        for ghost_arrow in self.pictograph.ghost_arrows.values():
            if self._is_arrow_movable(ghost_arrow):
                self._reposition_to_default_loc(ghost_arrow)

    ### HELPERS ###
    def _is_arrow_movable(self, arrow: Arrow) -> bool:
        return (
            not arrow.is_dragging
            and arrow.motion
            and arrow.motion.motion_type != STATIC
        )

    def compare_states(self, current_state: Dict, candidate_state: Dict) -> bool:
        relevant_keys = [
            "letter",
            "start_position",
            "end_position",
            "blue_motion_type",
            "blue_rotation_direction",
            "blue_turns",
            "blue_start_location",
            "blue_end_location",
            "red_motion_type",
            "red_rotation_direction",
            "red_turns",
            "red_start_location",
            "red_end_location",
        ]
        return all(
            current_state.get(key) == candidate_state.get(key) for key in relevant_keys
        )

    ### POSITIONING METHODS ###
    def _reposition_GH(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_GH_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_I(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_I_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)
            self._apply_adjustment(arrow.ghost, adjustment)

    def _reposition_P(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_P_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_Q(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_Q_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_R(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_R_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    ### ADJUSTMENT CALCULATIONS ###
    def _calculate_GH_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 105 if arrow.color == RED else 50
        return self.calculate_adjustment(arrow.location, distance)

    def _calculate_I_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 110 if arrow.motion_type == PRO else 55
        return self.calculate_adjustment(arrow.location, distance)

    def _calculate_P_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 90 if arrow.color == RED else 35
        return self.calculate_adjustment(arrow.location, distance)

    def _calculate_Q_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_dict = {
            RED: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(70, -110),
                    SOUTHEAST: QPointF(110, 70),
                    SOUTHWEST: QPointF(-70, 110),
                    NORTHWEST: QPointF(-110, -70),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(110, -70),
                    SOUTHEAST: QPointF(70, 110),
                    SOUTHWEST: QPointF(-110, 70),
                    NORTHWEST: QPointF(-70, -110),
                },
            },
            BLUE: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
            },
        }
        color_adjustments = adjustment_dict.get(arrow.color, {})
        rotation_adjustments = color_adjustments.get(
            arrow.motion.rotation_direction, {}
        )
        return rotation_adjustments.get(arrow.location, QPointF(0, 0))

    def _calculate_R_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_dict = {
            PRO: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(75, -60),
                    SOUTHEAST: QPointF(60, 75),
                    SOUTHWEST: QPointF(-75, 60),
                    NORTHWEST: QPointF(-60, -75),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(60, -75),
                    SOUTHEAST: QPointF(75, 60),
                    SOUTHWEST: QPointF(-60, 75),
                    NORTHWEST: QPointF(-75, -60),
                },
            },
            ANTI: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(35, -25),
                    SOUTHEAST: QPointF(25, 35),
                    SOUTHWEST: QPointF(-35, 25),
                    NORTHWEST: QPointF(-25, -35),
                },
            },
        }
        motion_type_adjustments = adjustment_dict.get(arrow.motion_type, {})
        rotation_adjustments = motion_type_adjustments.get(
            arrow.motion.rotation_direction, {}
        )
        return rotation_adjustments.get(arrow.location, QPointF(0, 0))

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
        default_pos = self._get_default_position(arrow)
        arrow_center = arrow.boundingRect().center()
        new_pos = default_pos - arrow_center + adjustment
        arrow.setPos(new_pos)

        # Update the ghost arrow with the same adjustment
        if update_ghost and arrow.ghost:
            self._apply_adjustment(arrow.ghost, adjustment, update_ghost=False)

    ### GETTERS ###
    def _get_default_position(self, arrow: Arrow) -> QPointF:
        layer2_points = self.pictograph.grid.get_layer2_points()
        return layer2_points.get(arrow.location, QPointF(0, 0))

    ### SETTERS ###
    def _set_arrow_to_optimal_loc(self, arrow: Arrow, optimal_locations: Dict) -> None:
        optimal_location = optimal_locations.get(f"optimal_{arrow.color}_location")
        if optimal_location:
            arrow.setPos(optimal_location - arrow.boundingRect().center())

    def _reposition_to_default_loc(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        # if the arrow isn't a Ghost Arrow itself,
        if not arrow.is_ghost:
            arrow.ghost.set_arrow_transform_origin_to_center()
        default_pos = self._get_default_position(arrow)
        adjustment = self.calculate_adjustment(arrow.location, DISTANCE)
        new_pos = default_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        if arrow.motion_type == ANTI and arrow.motion.prop.orientation in [
            CLOCK,
            COUNTER,
        ]:
            adjustment = self.calculate_adjustment(arrow.location, DISTANCE + -45)
            new_pos = default_pos + adjustment - arrow.boundingRect().center()
            arrow.setPos(new_pos)
