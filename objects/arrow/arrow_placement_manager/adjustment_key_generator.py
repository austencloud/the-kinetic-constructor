from typing import TYPE_CHECKING, Tuple
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.Letters import (
    Type1_hybrid_letters,
    Type3_letters,
    non_hybrid_letters,
    Type2_letters,
)
from constants import *

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class AdjustmentKeyGenerator:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.blue_arrow = self.pictograph.arrows.get(BLUE)
        self.red_arrow = self.pictograph.arrows.get(RED)

    def _normalize_arrow_turns(self, arrow: Arrow) -> int:
        """Convert arrow turns from float to int if they are whole numbers."""
        return int(arrow.turns) if arrow.turns in {0.0, 1.0, 2.0, 3.0} else arrow.turns

    def _generate_key_for_type1_hybrid(self) -> str:
        """Generate the key for Type1 hybrid letters."""
        pro_arrow, anti_arrow = self._get_pro_anti_arrows()
        return f"({pro_arrow.turns}, {anti_arrow.turns})"

    def _generate_key_for_type2(self) -> str:
        """Generate the key for Type2 letters, including 's' or 'o' based on rotation direction."""
        shift = self.red_arrow if self.red_arrow.motion.is_shift() else self.blue_arrow
        static = (
            self.red_arrow if self.red_arrow.motion.is_static() else self.blue_arrow
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

    def _generate_key_for_type3(self) -> str:
        """Generate the key for Type3 letters, including 's' or 'o' based on rotation direction."""
        shift = self.red_arrow if self.red_arrow.motion.is_shift() else self.blue_arrow
        dash = self.red_arrow if self.red_arrow.motion.is_dash() else self.blue_arrow
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

    def _generate_key_for_color(self) -> str:
        """Generate the key based on the color of the arrows."""
        return (
            f"({self._normalize_arrow_turns(self.blue_arrow)}, "
            f"{self._normalize_arrow_turns(self.red_arrow)})"
        )

    def _generate_key_for_s_t(self) -> str:
        """Generate the key for 'S' and 'T' letters based on leading and trailing states."""
        leading_motion = self.pictograph.get_leading_motion()
        trailing_motion = self.pictograph.get_trailing_motion()
        leading_motion.arrow.motion.lead_state = LEADING
        trailing_motion.arrow.motion.lead_state = TRAILING
        return f"({leading_motion.turns}, {trailing_motion.turns})"

    def _get_pro_anti_arrows(self) -> Tuple[Arrow, Arrow]:
        """Get the arrows corresponding to the pro and anti motions."""
        pro_arrow = (
            self.blue_arrow if self.blue_arrow.motion_type == PRO else self.red_arrow
        )
        anti_arrow = (
            self.blue_arrow if self.blue_arrow.motion_type == ANTI else self.red_arrow
        )
        return pro_arrow, anti_arrow

    def generate(self, letter) -> str:
        """Generate a key based on the letter and motion details."""
        key_handlers = {
            tuple(Type1_hybrid_letters): self._generate_key_for_type1_hybrid,
            ("S", "T"): self._generate_key_for_s_t,
            tuple(non_hybrid_letters): self._generate_key_for_color,
            tuple(Type2_letters): self._generate_key_for_type2,
            tuple(Type3_letters): self._generate_key_for_type3,
        }

        for key_set, handler in key_handlers.items():
            if letter in key_set:
                return handler()

        return ""
