from abc import ABC, abstractmethod
import json
from typing import TYPE_CHECKING, Dict, Tuple
from constants import ANTI, BLUE, FLOAT, PRO, RED, STATIC
from objects.motion.motion import Motion
from utilities.TypeChecking.Letters import (
    Letters,
    non_hybrid_letters,
    Type1_hybrid_letters,
    Type2_letters,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class LetterAdjustmentHandler(ABC):
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.red_motion = pictograph.red_motion
        self.blue_motion = pictograph.blue_motion

    def _update_or_create_turn_data(
        self, data: Dict, adjustment: Tuple[int, int], adjustment_key: str
    ):
        if adjustment_key not in data.get(self.pictograph.letter, {}):
            data[self.pictograph.letter] = {}
            data[self.pictograph.letter][adjustment_key] = self._get_default_turn_data()

        turn_data = data[self.pictograph.letter][adjustment_key]
        turn_data[self.pictograph.selected_arrow.color][0] += adjustment[0]
        turn_data[self.pictograph.selected_arrow.color][1] += adjustment[1]

    def _get_default_turn_data(self) -> Dict:
        default_data = self.load_json_data("arrow_placement/default_placements.json")

        motion_type = self.pictograph.selected_arrow.motion_type
        turns = str(self.pictograph.selected_arrow.turns)

        default_turn_data_for_selected_arrow = default_data.get(motion_type).get(turns)

        other_arrow = self.red_motion if self.pictograph.selected_arrow == self.blue_motion.arrow else self.blue_motion
        other_motion_type = other_arrow.motion_type
        other_turns = str(other_arrow.turns)
        default_turn_data_for_other_arrow = default_data.get(other_motion_type).get(other_turns)

        default_turn_data = {
            self.pictograph.selected_arrow.color: default_turn_data_for_selected_arrow,
            other_arrow.color: default_turn_data_for_other_arrow
        }
        return default_turn_data
    
    @abstractmethod
    def handle_adjustment(self, adjustment: Tuple[int, int]) -> None:
        pass

    def load_json_data(self, file_path) -> Dict:
        with open(file_path, "r") as file:
            return json.load(file)



class LetterAdjustmentHandlerFactory:
    def __init__(self, handler_map: Dict[str, LetterAdjustmentHandler]) -> None:
        self.handler_map = handler_map

    def create_handler(
        self, letter: str, pictograph: "Pictograph"
    ) -> LetterAdjustmentHandler:
        return self.handler_map.get(letter, DefaultLetterHandler)(pictograph)


class NonHybridLetterHandler(LetterAdjustmentHandler):
    def handle_adjustment(
        self, data: Dict[Letters, Dict], adjustment: Tuple[int, int]
    ) -> None:
        adjustment_key = self._get_adjustment_key_for_non_hybrid()
        self._update_or_create_turn_data(data, adjustment, adjustment_key)

    def _get_adjustment_key_for_non_hybrid(self) -> Tuple[int, int]:
        blue_turns = (
            int(self.blue_motion.turns)
            if self.blue_motion.turns in [0.0, 1.0, 2.0, 3.0]
            else self.blue_motion.turns
        )
        red_turns = (
            int(self.red_motion.turns)
            if self.red_motion.turns in [0.0, 1.0, 2.0, 3.0]
            else self.red_motion.turns
        )
        return (blue_turns, red_turns)


class Type1HybridLetterHandler(LetterAdjustmentHandler):
    def handle_adjustment(self, data: Dict, adjustment: Tuple[int, int]) -> None:
        self._initialize_pro_anti_motions()
        adjustment_key = f"{self.pro_motion.turns},{self.anti_motion.turns}"
        self._update_or_create_turn_data(data, adjustment, adjustment_key)

    def _initialize_pro_anti_motions(self) -> None:
        self.pro_motion = (
            self.red_motion if self.red_motion.motion_type == PRO else self.blue_motion
        )
        self.anti_motion = (
            self.blue_motion
            if self.blue_motion.motion_type == ANTI
            else self.red_motion
        )


class Type2LetterHandler(LetterAdjustmentHandler):
    def handle_adjustment(self, data: Dict, adjustment: Tuple[int, int]) -> None:
        shift_motion, static_motion = self._get_shift_static_motions()
        adjustment_key = self._construct_adjustment_key(shift_motion, static_motion)
        self._update_or_create_turn_data(data, adjustment, adjustment_key)

    def _get_shift_static_motions(self) -> Tuple[Motion, Motion]:
        shift_motion = (
            self.red_motion
            if self.red_motion.motion_type in [PRO, ANTI, FLOAT]
            else self.blue_motion
        )
        static_motion = (
            self.red_motion
            if self.red_motion.motion_type == STATIC
            else self.blue_motion
        )
        return shift_motion, static_motion

    def _construct_adjustment_key(self, shift_motion: Motion, static_motion: Motion):
        if static_motion.turns > 0:
            direction = (
                "opp"
                if static_motion.prop_rot_dir != shift_motion.prop_rot_dir
                else "same"
            )
            return f"({direction[0]}, {int(shift_motion.turns)}, {int(static_motion.turns)})"
        else:
            return f"({int(shift_motion.turns)}, {int(static_motion.turns)})"


class DefaultLetterHandler(LetterAdjustmentHandler):
    def handle_adjustment(self, data: Dict, adjustment: Tuple[int, int]) -> None:
        print(
            f"Warning: No specific adjustment handler for letter {self.pictograph.letter}. Using default handler."
        )
        if self.pictograph.selected_arrow:
            default_key = "default"
            self._update_or_create_turn_data(data, adjustment, default_key)
