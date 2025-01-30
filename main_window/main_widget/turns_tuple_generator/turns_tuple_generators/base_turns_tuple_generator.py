from typing import TYPE_CHECKING
from data.constants import BLUE, RED
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class BaseTurnsTupleGenerator:
    def _normalize_turns(self, motion: Motion) -> int:
        if motion.motion_data["turns"] == "fl":
            return "fl"
        return (
            int(motion.motion_data["turns"])
            if motion.motion_data["turns"] in {0.0, 1.0, 2.0, 3.0}
            else motion.motion_data["turns"]
        )

    def set_pictograph(self, pictograph: "BasePictograph"):
        self.pictograph = pictograph

        self.blue_motion = self.pictograph.motions.get(BLUE)
        self.red_motion = self.pictograph.motions.get(RED)

    def generate_turns_tuple(self, pictograph) -> str:
        pass
