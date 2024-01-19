from typing import TYPE_CHECKING, Optional, Tuple, Dict
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type2_letters,
    Type3_letters,
    non_hybrid_letters,
)

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class AdjustmentCalculator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def calculate_adjustment(
        self, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        placements = self.positioner.data_loader.load_placements()
        letter_data: Dict[str, Dict] = placements.get(
            self.positioner.pictograph.letter, {}
        )
        return letter_data.get(adjustment_key, {}).get(
            self.positioner.key_generator.determine_key(arrow)
        )

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, adjustment_key: str = None
    ) -> Optional[Tuple[int, int]]:
        if adjustment_key is None:
            adjustment_key = self.positioner.key_generator.determine_key(letter)
        self.special_placements: Dict[
            str, Dict
        ] = self.positioner.data_loader.load_placements()
        letter_adjustments: Dict = self.special_placements.get(letter, {}).get(
            adjustment_key, {}
        )

        adjustment_map = {
            "S": letter_adjustments.get(arrow.motion.lead_state),
            "T": letter_adjustments.get(arrow.motion.lead_state),
            **{
                letter: letter_adjustments.get(arrow.motion.motion_type)
                for letter in Type1_hybrid_letters
            },
            **{
                letter: letter_adjustments.get(arrow.color)
                for letter in non_hybrid_letters
            },
            **{
                letter: letter_adjustments.get(arrow.motion.motion_type)
                for letter in Type2_letters + Type3_letters
            },
        }

        return adjustment_map.get(letter)
