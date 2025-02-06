from typing import TYPE_CHECKING
from data.constants import BLUE, RED
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class BaseTurnsTupleGenerator:
    def _normalize_turns(self, motion: Motion) -> int:
        if motion.turns == "fl":
            return "fl"
        return (
            int(motion.turns) if motion.turns in {0.0, 1.0, 2.0, 3.0} else motion.turns
        )

    def set_pictograph(self, pictograph: "BasePictograph"):
        self.pictograph = pictograph

        self.blue_motion = self.pictograph.motions.get(BLUE)
        self.red_motion = self.pictograph.motions.get(RED)

    def generate_turns_tuple(self, pictograph) -> str:
        pass 
