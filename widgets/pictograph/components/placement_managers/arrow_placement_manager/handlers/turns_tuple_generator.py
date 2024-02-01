from typing import Union
from Enums import LetterType
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type1_non_hybrid_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
    Type2_letters,
)
from constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager
from .turns_tuple_generators import *


class TurnsTupleGenerator:
    def __init__(self) -> None:
        self.generators = {
            "Type1_hybrid": Type1HybridTurnsTupleGenerator(),
            "Type2": Type2TurnsTupleGenerator(),
            "Type3": Type3TurnsTupleGenerator(),
            "Type4": Type4TurnsTupleGenerator(),
            "Type56": Type56TurnsTupleGenerator(),
            "Color": ColorTurnsTupleGenerator(),
            "LeadState": LeadStateTurnsTupleGenerator(),
            "Lambda": LambdaTurnsTupleGenerator(),
            "LambdaDash": LambdaDashTurnsTupleGenerator(),
            "Gamma": GammaTurnsTupleGenerator(),
        }
        self.key_map = self._create_key_map()

    def _create_key_map(self):
        key_map = {
            "Λ": "Lambda",
            "Λ-": "LambdaDash",
            "Γ": "Gamma",
            ("S", "T"): "LeadState",
        }
        for letter in Type1_hybrid_letters:
            key_map[letter] = "Type1_hybrid"
        for letter in Type1_non_hybrid_letters:
            key_map[letter] = "Color"
        for letter in Type2_letters:
            key_map[letter] = "Type2"
        for letter in Type3_letters:
            key_map[letter] = "Type3"
        for letter in Type4_letters:
            key_map[letter] = "Type4"
        for letter in Type5_letters + Type6_letters:
            key_map[letter] = "Type56"
        return key_map

    def generate_turns_tuple(self, pictograph: "Pictograph") -> str:
        generator_key = self.key_map.get(pictograph.letter)
        if generator_key:
            return self.generators[generator_key].generate_key(pictograph)
        return ""

    def generate_mirrored_tuple(self, arrow: "Arrow") -> Union[str, None]:
        turns_tuple = self.generate_turns_tuple(arrow.pictograph)
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)

        mirrored_logic = {
            "Type1": self._handle_type1_mirroring,
            "Type4": self._handle_type4_mirroring,
            "Type56": self._handle_type56_mirroring,
        }

        return mirrored_logic.get(letter_type, lambda x: None)(turns_tuple)

    def _handle_type1_mirroring(self, turns_tuple):
        items = turns_tuple.strip("()").split(", ")
        return f"({items[1]}, {items[0]})"

    def _handle_type4_mirroring(self, turns_tuple):
        prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
        turns = turns_tuple[turns_tuple.find(",") + 2 :]
        return (
            f"({prop_rotation}, {turns})"
            if "cw" in turns_tuple or "ccw" in turns_tuple
            else None
        )

    def _handle_type56_mirroring(self, turns_tuple):
        items = turns_tuple.strip("()").split(", ")
        if len(items) == 3:
            return f"({items[0]}, {items[2]}, {items[1]})"
        prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
        turns = turns_tuple[turns_tuple.find(",") + 2 : -1]
        return f"({prop_rotation}, {turns})"
