from PyQt6.QtCore import QPointF
from Enums import Letter
from constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Callable, Dict, List, Union


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
        self.letters: Dict[
            Letter, List[Dict[str, str]]
        ] = pictograph.main_widget.letters
        self.letters_to_reposition: List[Letter] = ["G", "H", "I", "P", "Q", "R"]

    ### PUBLIC METHODS ###
    def update_arrow_positions(self) -> None:
        self.red_motion = self.pictograph.motions[RED]
        self.blue_motion = self.pictograph.motions[BLUE]
        self.red_arrow = self.pictograph.arrows[RED]
        self.blue_arrow = self.pictograph.arrows[BLUE]

        self.motions = self.pictograph.motions.values()
        self.arrows = self.pictograph.arrows.values()
        self.ghost_arrows = self.pictograph.ghost_arrows.values()

        self.current_letter = self.pictograph.current_letter

        for arrow in self.arrows:
            self._set_arrow_to_default_loc(arrow)

        for ghost_arrow in self.ghost_arrows:
            self._set_arrow_to_default_loc(ghost_arrow)

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
        if self.current_letter in ["G", "H"]:
            self._reposition_G_H()
        elif self.current_letter == "I":
            self._reposition_I()
        elif self.current_letter in ["P"]:
            self._reposition_P()
        elif self.current_letter in ["Q"]:
            self._reposition_Q()
        elif self.current_letter in ["R"]:
            self._reposition_R()

    def _calculate_adjustment_tuple(self, location: str, distance: int) -> QPointF:
        location_adjustments = {
            NORTHEAST: QPointF(distance, -distance),
            SOUTHEAST: QPointF(distance, distance),
            SOUTHWEST: QPointF(-distance, distance),
            NORTHWEST: QPointF(-distance, -distance),
        }
        return location_adjustments.get(location, QPointF(0, 0))

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
            "start_pos",
            "end_pos",
            BLUE_MOTION_TYPE,
            "blue_prop_rot_dir",
            "blue_turns",
            "blue_start_loc",
            "blue_end_loc",
            RED_MOTION_TYPE,
            "red_prop_rot_dir",
            "red_turns",
            "red_start_loc",
            "red_end_loc",
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

    def _set_arrow_to_default_loc(self, arrow: Arrow, _: Dict = None) -> None:
        arrow.set_arrow_transform_origin_to_center()
        # if the arrow isn't a Ghost Arrow itself,
        if not arrow.is_ghost:
            arrow.ghost.set_arrow_transform_origin_to_center()
        default_pos = self._get_default_position(arrow)
        adjustment = self.calculate_adjustment(arrow.location, DISTANCE)
        new_pos = default_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
