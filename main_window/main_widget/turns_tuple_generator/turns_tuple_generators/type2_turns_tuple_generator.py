from typing import TYPE_CHECKING
from data.constants import *
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class Type2TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph: "BasePictograph") -> str:
        super().set_pictograph(pictograph)

        shift = (
            self.red_motion if self.red_motion.check.is_shift() else self.blue_motion
        )
        static = (
            self.red_motion if self.red_motion.check.is_static() else self.blue_motion
        )
        # check if the letter is Omega
        if static.pictograph.letter.value == "Ω":
            print("static_pictograph_letter", static.pictograph.letter.value)
            print("Static Motion in Generator: ", static)
            print("static_turns", static.turns)

        if shift.motion_type in [PRO, ANTI]:
            if static.motion_dict["turns"] != 0 and static.prop_rot_dir != NO_ROT:
                direction = "s" if static.prop_rot_dir == shift.prop_rot_dir else "o"
                return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
            else:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(static)})"
                )
        elif shift.motion_type == FLOAT:
            if static.turns != 0 and static.prop_rot_dir != NO_ROT:
                direction = (
                    "s" if static.prop_rot_dir == shift.prefloat_prop_rot_dir else "o"
                )
                return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
            else:
                return (
                    f"({self._normalize_turns(shift)}, {self._normalize_turns(static)})"
                )
