import stat
from typing import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type1_non_hybrid_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
    Type2_letters,
)
from constants import *

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager


class TurnsTupleGenerator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.p = placement_manager.pictograph
        self.blue_arrow = self.p.arrows.get(BLUE)
        self.red_arrow = self.p.arrows.get(RED)

    def _normalize_arrow_turns(self, arrow: Arrow) -> int:
        """Convert arrow turns from float to int if they are whole numbers."""
        return int(arrow.turns) if arrow.turns in {0.0, 1.0, 2.0, 3.0} else arrow.turns

    def _generate_Type1_hybrid_key(self) -> str:
        """Generate the key for Type1 hybrid letters."""
        pro_arrow = (
            self.blue_arrow
            if self.blue_arrow.motion.motion_type == PRO
            else self.red_arrow
        )
        anti_arrow = (
            self.blue_arrow
            if self.blue_arrow.motion.motion_type == ANTI
            else self.red_arrow
        )
        return f"({pro_arrow.turns}, {anti_arrow.turns})"

    def _generate_Type2_key(self) -> str:
        """Generate the key for Type2 letters, including 's' or 'o' based on rotation direction."""
        shift = (
            self.red_arrow
            if self.red_arrow.motion.check.is_shift()
            else self.blue_arrow
        )
        static = (
            self.red_arrow
            if self.red_arrow.motion.check.is_static()
            else self.blue_arrow
        )
        if static.turns != 0 and static.motion.prop_rot_dir != NO_ROT:
            direction = (
                "s" if static.motion.prop_rot_dir == shift.motion.prop_rot_dir else "o"
            )
            return (
                f"({direction}, {self._normalize_arrow_turns(shift)}, "
                f"{self._normalize_arrow_turns(static)})"
            )
        else:
            return (
                f"({self._normalize_arrow_turns(shift)}, "
                f"{self._normalize_arrow_turns(static)})"
            )

    def _generate_Type3_key(self) -> str:
        """Generate the key for Type3 letters, including 's' or 'o' based on rotation direction."""
        shift = (
            self.red_arrow
            if self.red_arrow.motion.check.is_shift()
            else self.blue_arrow
        )
        dash = (
            self.red_arrow if self.red_arrow.motion.check.is_dash() else self.blue_arrow
        )
        if dash.turns != 0 and dash.motion.prop_rot_dir != NO_ROT:
            direction = (
                "s" if dash.motion.prop_rot_dir == shift.motion.prop_rot_dir else "o"
            )
            return (
                f"({direction}, {self._normalize_arrow_turns(shift)}, "
                f"{self._normalize_arrow_turns(dash)})"
            )
        else:
            return (
                f"({self._normalize_arrow_turns(shift)}, "
                f"{self._normalize_arrow_turns(dash)})"
            )

    def _generate_Type4_key(self) -> str:
        dash = self.p.get.dash()
        static = self.p.get.static()

        if dash.turns == 0 and static.turns == 0:
            return f"({self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)})"
        elif dash.turns == 0 or static.turns == 0:
            # One of the turns is zero, use the prop_rot_dir of the turning motion
            turning_motion = dash if dash.turns != 0 else static
            return f"({turning_motion.prop_rot_dir}, {self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)})"
        else:
            # Both have turns, use 's' or 'o'
            direction = "s" if dash.prop_rot_dir == static.prop_rot_dir else "o"
            return f"({direction}, {self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)})"

    def _generate_Type5_6_key(self) -> str:
        if self.blue_arrow.turns == 0 or self.red_arrow.turns == 0:
            # One of the turns is zero, use the prop_rot_dir of the turning arrow
            turning_arrow = (
                self.blue_arrow if self.blue_arrow.turns != 0 else self.red_arrow
            )
            return f"({turning_arrow.motion.prop_rot_dir}, {self._normalize_arrow_turns(self.blue_arrow)}, {self._normalize_arrow_turns(self.red_arrow)})"
        else:
            # Both have turns, use 's' or 'o'
            direction = (
                "s"
                if self.blue_arrow.motion.prop_rot_dir
                == self.red_arrow.motion.prop_rot_dir
                else "o"
            )
            return f"({direction}, {self._normalize_arrow_turns(self.blue_arrow)}, {self._normalize_arrow_turns(self.red_arrow)})"

    def _generate_color_key(self) -> str:
        """Generate the key based on the color of the arrows."""
        return (
            f"({self._normalize_arrow_turns(self.blue_arrow)}, "
            f"{self._normalize_arrow_turns(self.red_arrow)})"
        )

    def _generate_lead_state_key(self) -> str:
        """Generate the key for 'S' and 'T' letters based on leading and trailing states."""
        leading_motion = self.p.get.leading_motion()
        trailing_motion = self.p.get.trailing_motion()
        if leading_motion:
            leading_motion.arrow.motion.lead_state = LEADING
            trailing_motion.arrow.motion.lead_state = TRAILING
            return f"({leading_motion.turns}, {trailing_motion.turns})"
        else:
            return (
                f"({self._normalize_arrow_turns(self.blue_arrow)}, "
                f"{self._normalize_arrow_turns(self.red_arrow)})"
            )

    def _generate_Λ_key(self) -> str:
        # Determine the opening/closing direction
        dash = self.p.get.dash()
        static = self.p.get.static()
        dash_direction_map = {
            (EAST, NORTH, CLOCKWISE): OPENING,
            (EAST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (EAST, SOUTH, CLOCKWISE): CLOSING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, NORTH, CLOCKWISE): CLOSING,
            (WEST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, SOUTH, CLOCKWISE): OPENING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, EAST, CLOCKWISE): CLOSING,
            (NORTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (NORTH, WEST, CLOCKWISE): OPENING,
            (NORTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, EAST, CLOCKWISE): OPENING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, WEST, CLOCKWISE): CLOSING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): OPENING,
        }
        static_direction_map = {
            (EAST, NORTH, CLOCKWISE): CLOSING,
            (EAST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (EAST, SOUTH, CLOCKWISE): OPENING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, NORTH, CLOCKWISE): OPENING,
            (WEST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, SOUTH, CLOCKWISE): CLOSING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (NORTH, EAST, CLOCKWISE): OPENING,
            (NORTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, WEST, CLOCKWISE): CLOSING,
            (NORTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, EAST, CLOCKWISE): CLOSING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, WEST, CLOCKWISE): OPENING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): CLOSING,
        }
        if dash.turns == 0 and static.turns > 0:
            static_open_close_state = static_direction_map.get(
                (dash.end_loc, static.end_loc, static.prop_rot_dir), ""
            )
            return f"({self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)}, {static_open_close_state})"

        elif static.turns == 0 and dash.turns > 0:
            dash_open_close_state = dash_direction_map.get(
                (dash.end_loc, static.end_loc, dash.prop_rot_dir), ""
            )
            return f"({self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)}, {dash_open_close_state})"

        elif static.turns > 0 and dash.turns > 0:
            static_open_close_state = static_direction_map.get(
                (dash.end_loc, static.end_loc, static.prop_rot_dir), ""
            )
            dash_open_close_state = dash_direction_map.get(
                (dash.end_loc, static.end_loc, dash.prop_rot_dir), ""
            )
            vtg_dir = SAME if static.prop_rot_dir == dash.prop_rot_dir else OPP
            return f"({vtg_dir[0]}, {self._normalize_arrow_turns(dash)}, {self._normalize_arrow_turns(static)}, {dash_open_close_state}, {static_open_close_state})"

    def _generate_Λ_dash_key(self, blue_dash, red_dash) -> str:
        # Determine the opening/closing direction for Λ-
        open_close_state = self._determine_lambda_open_close_state(blue_dash, red_dash)

        # Generate the tuple key for Λ-
        return f"({blue_dash.motion.prop_rot_dir}, {self._normalize_arrow_turns(blue_dash)}, {self._normalize_arrow_turns(red_dash)}, {open_close_state})"

    def generate_turns_tuple(self, letter: Letters) -> str:
        """Generate a key based on the letter and motion details."""
        key_handlers = {
            tuple(Type1_hybrid_letters): self._generate_Type1_hybrid_key,
            ("S", "T"): self._generate_lead_state_key,
            tuple(Type1_non_hybrid_letters): self._generate_color_key,
            tuple(Type2_letters): self._generate_Type2_key,
            tuple(Type3_letters): self._generate_Type3_key,
            ("Λ"): self._generate_Λ_key,
            ("Λ-"): self._generate_Λ_dash_key,
            tuple(Type4_letters): self._generate_Type4_key,
            tuple(Type5_letters + Type6_letters): self._generate_Type5_6_key,
        }

        for key_set, handler in key_handlers.items():
            if letter in key_set:
                return handler()

        return ""
