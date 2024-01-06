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


class E_Positioner:
    def __init__(
        self, pictograph: "Pictograph", positioner: "Type1ArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.positioner = positioner

    def _load_adjustments(self) -> Dict[str, Dict[MotionTypes, List[int]]]:
        json_path = "arrow_adjuster/E_adjustments.json"
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

