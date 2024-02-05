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
from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.mirrored_turns_tuple_generator import (
    MirroredTurnsTupleGenerator,
)


from .turns_tuple_generators import *


class TurnsTupleGenerator:
    """
    Manages the generation of turn tuples for different letter types in a pictograph.
    It delegates to specific generator classes based on letter type.

    Attributes:
        generators (dict): Maps generator keys to specialized generator instances for various letter types.
        mirrored_generator (MirroredTurnsTupleGenerator): Handles mirrored turn tuple generation.

    Methods:
        generate_turns_tuple(pictograph: "Pictograph") -> str: Returns turn tuple for a pictograph based on its letter.
        generate_mirrored_tuple(arrow: "Arrow") -> Union[str, None]: Returns mirrored turn tuple for an arrow.

    The class ensures accurate and efficient generation of turn tuples, prioritizing special cases like S, T, Λ, Λ-, and Γ.
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
        self.mirrored_generator = MirroredTurnsTupleGenerator(self)

    def generate_turns_tuple(self, pictograph: "Pictograph") -> str:
        generator_key = self._get_generator_key(pictograph.letter)
        if generator_key:
            return self.generators[generator_key].generate_key(pictograph)
        return ""

    def generate_mirrored_tuple(self, arrow: "Arrow") -> Union[str, None]:
        return self.mirrored_generator.generate(arrow)

    def _get_generator_key(self, letter: str) -> str:
        special_generators = {
            "S": "LeadState",
            "T": "LeadState",
            "Λ": "Lambda",
            "Λ-": "LambdaDash",
            "Γ": "Gamma",
        }
        general_generators = {
            letter: generator_key
            for generator_key, letters in {
                "Type1_hybrid": Type1_hybrid_letters,
                "Color": Type1_non_hybrid_letters,
                "Type2": Type2_letters,
                "Type3": Type3_letters,
                "Type4": Type4_letters,
                "Type56": Type5_letters + Type6_letters,
            }.items()
            for letter in letters
        }
        return special_generators.get(letter, general_generators.get(letter, ""))
