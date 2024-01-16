from PyQt6.QtCore import QPointF
from constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Literal, Tuple

from objects.arrow.arrow_placement_manager.adjustment_key_generator import (
    AdjustmentKeyGenerator,
)
from objects.arrow.arrow_placement_manager.directional_tuple_generator import (
    DirectionalTupleGenerator,
)
from .default_arrow_placement_manager import DefaultArrowPlacementManager
from .special_arrow_placement_manager import SpecialArrowPlacementManager
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors, Locations

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class ArrowPlacementManager:
    """Manages the placement of main arrows within the pictograph based on specific rules and letter types."""

    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.blue_arrow = self.pictograph.arrows.get(BLUE)
        self.red_arrow = self.pictograph.arrows.get(RED)
        self.default_manager = DefaultArrowPlacementManager(pictograph, self)
        self.special_placement_manager = SpecialArrowPlacementManager(pictograph, self)
        self.key_generator = AdjustmentKeyGenerator(self.pictograph)

    def reposition_for_letter(self, letter: str) -> None:
        """Reposition arrows based on the specified letter."""
        reposition_method = getattr(self, f"_reposition_{letter}", None)
        if reposition_method:
            reposition_method()

    def _get_diamond_shift_quadrant_index(
        self, location: Locations
    ) -> Literal[0, 1, 2, 3]:
        """Map location to index for quadrant adjustments"""
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }

        return location_to_index.get(location, 0)

    def _get_diamond_static_dash_quadrant_index(
        self, location: Locations
    ) -> Literal[0, 1, 2, 3]:
        """Map location to index for quadrant adjustments"""
        location_to_index = {
            NORTH: 0,
            EAST: 1,
            SOUTH: 2,
            WEST: 3,
        }

        return location_to_index.get(location, 0)

    def update_arrow_placement(self) -> None:
        """Update the placement of all arrows."""
        self.letter = self.pictograph.letter
        for arrow in self.pictograph.arrows.values():
            if arrow.loc:
                self._update_arrow_position(arrow)

    def _update_arrow_position(self, arrow: Arrow) -> None:
        """Calculate and update the position of a single arrow."""
        initial_pos = self._get_initial_pos(arrow)
        adjustment = self._get_adjustment(arrow)
        new_pos = initial_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        arrow.arrow_rot_angle_manager.update_rotation()

    def _get_initial_pos(self, arrow: Arrow) -> QPointF:
        if arrow.motion_type in [PRO, ANTI]:
            return self._get_diamond_shift_pos(arrow)
        elif arrow.motion_type in [STATIC, DASH]:
            return self._get_diamond_static_dash_pos(arrow)

    def _get_diamond_shift_pos(self, arrow: Arrow) -> QPointF:
        return self.pictograph.grid.circle_coordinates_cache["layer2_points"][
            self.pictograph.main_widget.grid_mode
        ]["normal"][f"{arrow.loc}_{self.pictograph.main_widget.grid_mode}_layer2_point"]

    def _get_diamond_static_dash_pos(self, arrow: Arrow) -> QPointF:
        return self.pictograph.grid.circle_coordinates_cache["hand_points"][
            self.pictograph.main_widget.grid_mode
        ]["normal"][f"{arrow.loc}_{self.pictograph.main_widget.grid_mode}_hand_point"]

    def _get_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_key = self.generate_adjustment_key()
        self.special_placement_manager.special_placements = (
            self.special_placement_manager._load_placements()
        )

        if self.letter in self.special_placement_manager.special_placements:
            special_adjustment = (
                self.special_placement_manager.get_adjustment_for_letter(
                    self.letter, arrow, adjustment_key
                )
            )
            if special_adjustment:
                x, y = special_adjustment
            else:
                x, y = self.default_manager.get_default_adjustment(arrow)
        else:
            x, y = self.default_manager.get_default_adjustment(arrow)
        directional_generator = DirectionalTupleGenerator(
            arrow.motion, self._get_other_motion(arrow.motion)
        )
        directional_adjustments = directional_generator.generate_directional_tuples(
            x, y
        )
        quadrant_index = self._get_quadrant_index(arrow)
        return QPointF(*directional_adjustments[quadrant_index])

    def _get_other_motion(self, motion: Motion) -> Motion:
        return (
            motion.scene.red_motion
            if motion.scene.red_motion != motion
            else motion.scene.blue_motion
        )

    def _get_quadrant_index(self, arrow: Arrow) -> Literal[0, 1, 2, 3]:
        if self.pictograph.grid.grid_mode == DIAMOND:
            if arrow.motion_type in [PRO, ANTI]:
                return self._get_diamond_shift_quadrant_index(arrow.loc)
            elif arrow.motion_type in [STATIC, DASH]:
                return self._get_diamond_static_dash_quadrant_index(arrow.loc)

    def _convert_turns_to_int(self, arrow):
        """Convert arrow turns from float to int if they are whole numbers."""
        if arrow.turns in [0.0, 1.0, 2.0, 3.0]:
            arrow.turns = int(arrow.turns)

    def _generate_pro_anti_key(self):
        """Generate the key for Type1 hybrid letters."""
        pro_arrow, anti_arrow = self._get_pro_anti_arrows()
        return f"({pro_arrow.turns}, {anti_arrow.turns})"

    def _generate_color_key(self):
        """Generate the color key for non-hybrid letters."""
        return f"({self.blue_arrow.turns}, {self.red_arrow.turns})"

    def _generate_shift_static_key(self):
        """Generate the key for Type2 letters."""
        shift = self.red_arrow if self.red_arrow.motion.is_shift() else self.blue_arrow
        static = (
            self.red_arrow if self.red_arrow.motion.is_static() else self.blue_arrow
        )
        return f"({shift.turns}, {static.turns})"

    def _generate_lead_state_key(self):
        """Generate the lead state key for 'S' and 'T' letters."""
        leading_motion = self.pictograph.get_leading_motion()
        trailing_motion = self.pictograph.get_trailing_motion()
        leading_motion.arrow.motion.lead_state = LEADING
        trailing_motion.arrow.motion.lead_state = TRAILING
        return f"({leading_motion.turns}, {trailing_motion.turns})"

    def generate_adjustment_key(self) -> str:
        """Generate a unique key to determine arrow adjustment based on the letter."""
        return self.key_generator.generate(self.pictograph.letter)

    def _get_pro_anti_arrows(self) -> Tuple[Arrow, Arrow]:
        pro_arrow = (
            self.blue_arrow if self.blue_arrow.motion_type == PRO else self.red_arrow
        )
        anti_arrow = (
            self.blue_arrow if self.blue_arrow.motion_type == ANTI else self.red_arrow
        )
        return pro_arrow, anti_arrow

    def determine_leading_color(
        self, red_start, red_end, blue_start, blue_end
    ) -> Colors:
        if red_start == blue_end:
            return RED
        elif blue_start == red_end:
            return BLUE
        return None

    def get_opposite_location(self, location: str) -> str:
        opposite_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_map.get(location, "")

    def are_adjacent_locations(self, location1: str, location2: str) -> bool:
        adjacent_map = {
            NORTHEAST: [NORTH, EAST],
            SOUTHEAST: [SOUTH, EAST],
            SOUTHWEST: [SOUTH, WEST],
            NORTHWEST: [NORTH, WEST],
        }
        return location2 in adjacent_map.get(location1, [])
