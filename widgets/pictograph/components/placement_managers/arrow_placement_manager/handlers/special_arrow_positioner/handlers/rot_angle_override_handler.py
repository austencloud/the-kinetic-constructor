from typing import TYPE_CHECKING, Dict, Optional
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class RotAngleOverrideHandler:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = self.positioner.data_loader.load_placements()
        letter_data: Dict[str, Dict] = placements.get(
            self.positioner.pictograph.letter, {}
        )
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
            arrow.scene.letter
        )
        return letter_data.get(turns_tuple, {}).get(
            f"{arrow.motion.motion_type}_rot_angle"
        )
