import json
from typing import TYPE_CHECKING, Dict, Optional, Tuple
from constants import BLUE, LEADING, RED, TRAILING

from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from utilities.TypeChecking.Letters import (
    Type1_hybrid_letters,
    Type1_non_hybrid_letters,
    Type2_letters,
)
from utilities.TypeChecking.TypeChecking import Colors


if TYPE_CHECKING:
    from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
        MainArrowPlacementManager,
    )
    from objects.pictograph.pictograph import Pictograph


class SpecialArrowPlacementManager:
    def __init__(
        self,
        pictograph: "Pictograph",
        main_arrow_placement_manager: "MainArrowPlacementManager",
    ) -> None:
        self.pictograph = pictograph
        self.main_arrow_placement_manager = main_arrow_placement_manager
        self.blue_arrow = self.pictograph.arrows.get(BLUE)
        self.red_arrow = self.pictograph.arrows.get(RED)
        self.special_placements = self._load_placements()

    def _load_placements(self) -> Dict[str, Dict[str, Tuple[int, int]]]:
        json_path = "arrow_placement/special_placements.json"
        with open(json_path, "r") as file:
            return json.load(file)

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        self.special_placements = self._load_placements()
        letter_adjustments = self.special_placements.get(letter, {}).get(
            adjustment_key, {}
        )
        if letter in Type1_hybrid_letters or letter in Type2_letters:
            return letter_adjustments.get(arrow.motion_type)
        elif letter in ["S", "T"]:
            leading_motion = self.pictograph.get_leading_motion()
            trailing_motion = (
                self.blue_arrow.motion
                if leading_motion == self.red_arrow.motion
                else self.red_arrow.motion
            )
            leading_motion.arrow.lead_state = LEADING
            trailing_motion.arrow.lead_state = TRAILING

            return letter_adjustments.get(arrow.lead_state)
        elif letter in Type1_non_hybrid_letters:
            return letter_adjustments.get(arrow.color)
        return None

    def _adjustment_for_E(self, arrow: Arrow) -> Tuple[int, int]:
        adjustment_key = f"({self.blue_arrow.turns}, {self.red_arrow.turns})"
        special_keys = ["(0.5, 0.5)", "(2.5, 2.5)", "(0.5, 2.5)", "(2.5, 0.5)"]
        if adjustment_key in special_keys:
            return (
                self.special_placements.get(self.pictograph.letter, {})
                .get(adjustment_key, {})
                .get(arrow.color, (0, 0))
            )
        return (0, 0)

    def _adjustment_for_U(self, arrow: Arrow) -> Tuple[int, int]:
        pro_arrow, anti_arrow = self.main_arrow_placement_manager._get_pro_anti_arrows()
        adjustment_key = f"({pro_arrow.turns}, {anti_arrow.turns})"
        special_keys = [
            "(1, 0.5)",
            "(1, 1.5)",
            "(1, 2.5)",
            "(1.5, 0.5)",
            "(1.5, 2.5)",
            "(2, 0.5)",
            "(2, 1.5)",
            "(2, 2.5)",
            "(2.5, 1.5)",
            "(3, 0.5)",
            "(3, 1.5)",
            "(3, 2.5)",
        ]
        if adjustment_key in special_keys:
            return (
                self.special_placements.get(self.pictograph.letter, {})
                .get(adjustment_key, {})
                .get(arrow.motion_type, (0, 0))
            )
        return (0, 0)

    def _adjustment_for_V(self, arrow: Arrow) -> Tuple[int, int]:
        pro_arrow, anti_arrow = self.main_arrow_placement_manager._get_pro_anti_arrows()
        adjustment_key = f"({pro_arrow.turns}, {anti_arrow.turns})"
        special_keys = [
            "(0, 0.5)",
            "(0, 1.5)",
            "(0, 2.5)",
            "(0.5, 0)",
            "(0.5, 0.5)",
            "(0.5, 1)",
            "(0.5, 2)",
            "(0.5, 2.5)",
            "(0.5, 3)",
            "(1, 0.5)",
            "(1, 1.5)",
            "(1, 2.5)",
            "(1.5, 0)",
            "(1.5, 1.5)",
            "(1.5, 2.5)",
            "(2, 0.5)",
            "(2, 1.5)",
            "(2, 2.5)",
            "(2.5, 0)",
            "(2.5, 0.5)",
            "(2.5, 1.5)",
            "(2.5, 2.5)",
            "(3, 0.5)",
            "(3, 1.5)",
            "(3, 2.5)",
        ]
        if adjustment_key in special_keys:
            return (
                self.special_placements.get(self.pictograph.letter, {})
                .get(adjustment_key, {})
                .get(arrow.motion_type, (0, 0))
            )
        return (0, 0)

    def _get_special_adjustment(
        self, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        letter_adjustments = self.special_placements.get(
            self.pictograph.letter, {}
        ).get(adjustment_key, {})

        if (
            self.pictograph.letter in Type1_hybrid_letters
            or self.pictograph.letter in Type2_letters
        ):
            return letter_adjustments.get(arrow.motion_type)
        elif self.pictograph.letter in Type1_non_hybrid_letters:
            return letter_adjustments.get(arrow.color)

        return None

    def _convert_key_to_tuple(self, key: str) -> Tuple[int, int]:
        key_values = key.strip("()").split(", ")
        converted_values = []
        for value in key_values:
            if value.isdigit() and int(value) in [0, 1, 2, 3]:
                converted_values.append(int(value))
            else:
                converted_values.append(float(value))
        return tuple(converted_values)
