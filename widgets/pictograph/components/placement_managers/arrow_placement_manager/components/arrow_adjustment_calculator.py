import re
from PyQt6.QtCore import QPointF
from Enums.letters import Letter
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Optional

from .directional_tuple_manager.directional_tuple_manager import DirectionalTupleManager


if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager


class ArrowAdjustmentCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager

    # @lru_cache
    def get_adjustment(self, arrow: Arrow) -> QPointF:
        
        if not arrow.motion.pictograph.letter:
            return
        turns_tuple = (
            arrow.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
                self.placement_manager.pictograph
            )
        )
        ori_key = self.placement_manager.special_positioner.data_updater.get_ori_key(
            arrow.motion
        )
        special_placements = (
            self.placement_manager.pictograph.main_widget.special_placements[ori_key]
        )

        if not self.placement_manager.pictograph.letter in special_placements:
            special_placements[self.placement_manager.pictograph.letter] = {}
        if self.placement_manager.pictograph.letter in special_placements:
            special_adjustment = self.get_adjustment_for_letter(
                self.placement_manager.pictograph.letter, arrow, turns_tuple, ori_key
            )
            (
                x,
                y,
            ) = (
                special_adjustment
                or self.placement_manager.default_positioner.get_default_adjustment(
                    arrow
                )
            )
        else:
            x, y = self.placement_manager.default_positioner.get_default_adjustment(
                arrow
            )

        directional_tuple_manager = DirectionalTupleManager(arrow.motion)
        directional_adjustments = directional_tuple_manager.generate_directional_tuples(
            x, y
        )
        quadrant_index = (
            self.placement_manager.quadrant_index_handler.get_quadrant_index(arrow)
        )
        return QPointF(*directional_adjustments[quadrant_index])

    def _find_special_rotation(self, turn_data: dict) -> Optional[dict]:
        for key, value in turn_data.items():
            if re.match(r"^(cw|ccw)_static$", key):
                return value
        return None

    def get_adjustment_for_letter(
        self, letter: Letter, arrow: Arrow, turns_tuple: str, ori_key: str
    ) -> Optional[tuple[int, int]]:
        self.special_placements: dict[str, dict] = (
            self.placement_manager.pictograph.main_widget.special_placements[ori_key]
        )
        letter_adjustments: dict[str, dict[str, list]] = self.special_placements.get(
            letter.value, {}
        ).get(turns_tuple, {})

        key = self.placement_manager.special_positioner.attr_key_generator.get_key(
            arrow
        )
        # check if the key is a str
        if isinstance(key, str):

            return letter_adjustments.get(key)
        else:
            return letter_adjustments.get(key.value)
