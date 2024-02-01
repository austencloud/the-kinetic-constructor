import re
from PyQt6.QtCore import QPointF
from constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Optional

from .directional_tuple_generator import DirectionalTupleGenerator

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager


class ArrowAdjustmentCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.pm = placement_manager

    def get_adjustment(self, arrow: Arrow) -> QPointF:
        turns_tuple = arrow.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
            self.pm.pictograph
        )
        ori_key = self.pm.special_positioner.data_updater._get_ori_key(arrow.motion)
        special_placements = self.pm.pictograph.main_widget.special_placements[ori_key]

        if not self.pm.pictograph.letter in special_placements:
            special_placements[self.pm.pictograph.letter] = {}
        if self.pm.pictograph.letter in special_placements:
            special_adjustment = self.get_adjustment_for_letter(
                self.pm.pictograph.letter, arrow, turns_tuple, ori_key
            )
            (
                x,
                y,
            ) = special_adjustment or self.pm.default_positioner.get_default_adjustment(
                arrow
            )
        else:
            x, y = self.pm.default_positioner.get_default_adjustment(arrow)

        directional_generator = DirectionalTupleGenerator(
            arrow.motion, arrow.pictograph.get.other_motion(arrow.motion)
        )
        directional_adjustments = directional_generator.generate_directional_tuples(
            x, y
        )
        quadrant_index = self.pm.quadrant_index_handler.get_quadrant_index(arrow)
        return QPointF(*directional_adjustments[quadrant_index])

    def _find_special_rotation(self, turn_data: dict) -> Optional[dict]:
        for key, value in turn_data.items():
            if re.match(r"^(cw|ccw)_static$", key):
                return value
        return None

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, turns_tuple: str, ori_key: str
    ) -> Optional[tuple[int, int]]:
        self.special_placements: dict[str, dict] = (
            self.pm.pictograph.main_widget.special_placements[ori_key]
        )
        letter_adjustments: dict[str, dict[str, list]] = self.special_placements.get(
            letter
        ).get(turns_tuple, {})

        key = self.pm.special_positioner.attr_key_generator.get_key(arrow)

        return letter_adjustments.get(key)
