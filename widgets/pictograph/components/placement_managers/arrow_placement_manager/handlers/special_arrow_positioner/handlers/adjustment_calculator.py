from typing import TYPE_CHECKING, Optional, Tuple, Dict
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    non_hybrid_letters,
)

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class AdjustmentCalculator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def calculate_turns_tuple(
        self, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        placements = self.positioner.placement_manager.pictograph.main_widget.special_placements
        letter_data: Dict[str, Dict] = placements.get(
            self.positioner.pictograph.letter, {}
        )
        return letter_data.get(adjustment_key, {}).get(
            self.positioner.turns_tuple_generator.generate_turns_tuple(arrow)
        )

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, turns_tuple: str = None
    ) -> Optional[Tuple[int, int]]:
        if turns_tuple is None:
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                arrow
            )
        self.special_placements: Dict[
            str, Dict
        ] = self.positioner.placement_manager.pictograph.main_widget.special_placements
        letter_adjustments: Dict = self.special_placements.get(letter, {}).get(
            turns_tuple, {}
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
                if letter not in ["S", "T"]
            },
            **{
                letter: letter_adjustments.get(arrow.motion.motion_type)
                for letter in Type2_letters + Type3_letters + Type4_letters
            },
        }

        return adjustment_map.get(letter)
