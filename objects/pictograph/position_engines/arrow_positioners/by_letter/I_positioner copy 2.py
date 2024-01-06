import json
from typing import TYPE_CHECKING, Dict, List, Literal, Tuple
from constants import *
from PyQt6.QtCore import QPointF
from objects.arrow import Arrow
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import MotionTypes

if TYPE_CHECKING:
    from objects.pictograph.position_engines.arrow_positioners.Type1_arrow_positioner import (
        Type1ArrowPositioner,
    )
    from objects.pictograph.pictograph import Pictograph


class I_Positioner:
    def __init__(
        self, pictograph: "Pictograph", positioner: "Type1ArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.positioner = positioner

    def _load_adjustments(self) -> Dict[str, Dict[MotionTypes, List[int]]]:
        json_path = (
            "F:/CODE/tka-app/tka-sequence-constructor/arrow_adjuster/I_adjustments.json"
        )
        with open(json_path, "r") as file:
            data = json.load(file)

        # Convert string keys to tuples
        adjustments = {}
        for key, value in data.items():
            tuple_key = self._convert_key_to_tuple(key)
            adjustments[tuple_key] = value
        return adjustments

    def _convert_key_to_tuple(self, key: str) -> Tuple[int, int]:
        key_values = key.strip("()").split(", ")
        converted_values = []
        for value in key_values:
            if value.isdigit() and int(value) in [0, 1, 2, 3]:
                converted_values.append(int(value))
            else:
                converted_values.append(float(value))
        return tuple(converted_values)

    def _reposition_I(self) -> None:
        for arrow in self.pictograph.arrows.values():
            adjustment = self._calculate_I_adjustment(arrow)
            self.positioner._apply_shift_adjustment(arrow, adjustment)

    def _calculate_I_adjustment(self, arrow: Arrow) -> QPointF:
        self.adjustments: Dict[
            str, Dict[MotionTypes, List[int]]
        ] = self._load_adjustments()
        pro_arrow, anti_arrow = self._get_pro_anti_arrows(arrow.scene)
        if pro_arrow.turns in [0.0, 1.0, 2.0, 3.0]:
            pro_arrow.turns = int(pro_arrow.turns)
        if anti_arrow.turns in [0.0, 1.0, 2.0, 3.0]:
            anti_arrow.turns = int(anti_arrow.turns)
        adjustment_key = (pro_arrow.turns, anti_arrow.turns)

        ne_adjustment_values = self.adjustments.get(adjustment_key).get(
            arrow.motion_type
        )
        x, y = ne_adjustment_values
        if arrow.motion_type == PRO:
            directional_adjustments = self.generate_pro_directional_tuples(
                x, y, arrow.motion
            )
        elif arrow.motion_type == ANTI:
            directional_adjustments = self.generate_anti_directional_tuples(
                x, y, arrow.motion
            )
        return directional_adjustments[self._get_quadrant_index(arrow.loc)]

    def generate_pro_directional_tuples(self, x, y, motion: Motion) -> List[QPointF]:
        if motion.prop_rot_dir == CLOCKWISE:
            return [QPointF(x, y), QPointF(-y, x), QPointF(-x, -y), QPointF(y, -x)]
        elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return [QPointF(-y, -x), QPointF(x, -y), QPointF(y, x), QPointF(-x, y)]

    def generate_anti_directional_tuples(self, x, y, motion: Motion) -> List[QPointF]:
        if motion.prop_rot_dir == CLOCKWISE:
            return [QPointF(-y, -x), QPointF(x, -y), QPointF(y, x), QPointF(-x, y)]
        elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return [QPointF(x, y), QPointF(-y, x), QPointF(-x, -y), QPointF(y, -x)]

    def _get_quadrant_index(self, location: str) -> Literal[0, 1, 2, 3]:
        """Map location to index for quadrant adjustments"""
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)

    def _get_pro_anti_arrows(self, scene: "Pictograph") -> Tuple[Arrow, Arrow]:
        arrows = scene.arrows
        pro_arrow = arrows[RED] if arrows[RED].motion_type == PRO else arrows[BLUE]
        anti_arrow = arrows[RED] if arrows[RED].motion_type == ANTI else arrows[BLUE]
        return pro_arrow, anti_arrow

