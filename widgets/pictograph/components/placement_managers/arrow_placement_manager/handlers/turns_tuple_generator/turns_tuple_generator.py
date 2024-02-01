from typing import Union
from objects.arrow.arrow import Arrow
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

from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.turns_tuple_generator.mirrored_turns_tuple_generator import (
    MirroredTurnsTupleGenerator,
)
from .turns_tuple_generators import *


class TurnsTupleGenerator:
    """
    Manages the generation of turn tuples for different letter types in a pictograph. 
    It delegates to specific generator classes based on letter type.

    Attributes:
        generators (dict): Maps generator keys to specialized generator instances for various letter types.
        key_map (dict): Maps letters to generator keys, with special handling for 'S', 'T', 'Λ', 'Λ-', and 'Γ'.
        mirrored_generator (MirroredTurnsTupleGenerator): Handles mirrored turn tuple generation.

    Methods:
        _create_key_map(): Initializes the letter-to-generator key mapping.
        generate_turns_tuple(pictograph: "Pictograph") -> str: Returns turn tuple for a pictograph based on its letter.
        generate_mirrored_tuple(arrow: "Arrow") -> Union[str, None]: Returns mirrored turn tuple for an arrow.

    The class ensures accurate and efficient generation of turn tuples, prioritizing special cases like 'S' and 'T'.
    """

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
        self.mirrored_generator = MirroredTurnsTupleGenerator(self)

    def _create_key_map(self):
        key_map = {
            "S": "LeadState",
            "T": "LeadState",
            "Λ": "Lambda",
            "Λ-": "LambdaDash",
            "Γ": "Gamma",
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
        return self.mirrored_generator.generate(arrow)
