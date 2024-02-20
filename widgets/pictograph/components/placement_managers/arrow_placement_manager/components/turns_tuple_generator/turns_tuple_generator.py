from functools import lru_cache
from typing import Union
from Enums.Enums import LetterType, Letter

from Enums.letters import LetterConditions
from constants import *
from objects.arrow.arrow import Arrow
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

    def __init__(self):
        self.generators: list[BaseTurnsTupleGenerator] = {
            "Type1Hybrid": Type1HybridTurnsTupleGenerator(),
            "Type1NonHybrid": ColorTurnsTupleGenerator(),
            LetterType.Type2: Type2TurnsTupleGenerator(),
            LetterType.Type3: Type3TurnsTupleGenerator(),
            LetterType.Type4: Type4TurnsTupleGenerator(),
            LetterType.Type5: ColorTurnsTupleGenerator(),
            LetterType.Type6: ColorTurnsTupleGenerator(),
            # Add other types as needed
            "LeadState": LeadStateTurnsTupleGenerator(),
            "Lambda": LambdaTurnsTupleGenerator(),
            "LambdaDash": LambdaDashTurnsTupleGenerator(),
            "Gamma": GammaTurnsTupleGenerator(),
        }
        self.mirrored_generator = MirroredTurnsTupleGenerator(self)

    def generate_turns_tuple(self, pictograph: "Pictograph") -> str:
        generator_key = self._get_generator_key(pictograph.letter)
        if generator_key and generator_key in self.generators:
            generator = self.generators[generator_key]
            return generator.generate_turns_tuple(pictograph)
        return ""

    def generate_mirrored_tuple(self, arrow: Arrow) -> Union[str, None]:
        return self.mirrored_generator.generate(arrow)

    @lru_cache(maxsize=128)
    def _get_generator_key(self, letter: Letter) -> str:
        if letter.value in [
            letter.value
            for letter in letter.get_letters_by_condition(LetterConditions.TYPE1_HYBRID)
        ]:
            return "Type1Hybrid"
        elif letter.value in [
            letter.value
            for letter in letter.get_letters_by_condition(
                LetterConditions.TYPE1_NON_HYBRID
            )
        ]:
            return "Type1NonHybrid"
        special_cases = {
            "S": "LeadState",
            "T": "LeadState",
            "Λ": "Lambda",
            "Λ-": "LambdaDash",
            "Γ": "Gamma",
        }
        if letter.value in special_cases:
            return special_cases[letter.value]

        for letter_type in LetterType:
            if letter.value in letter_type.value[0]:
                return letter_type

        return None
