from typing import *

from Enums import (
    Letter,
    Location,
    MotionAttributesDicts,
    PictographAttribute,
    SpecificStartEndPositionsDicts,
)
from .Letters import *
from typing import Literal
from constants.constants import *
from enum import Enum
from typing import Dict
from Enums import MotionTypeCombination


Turns = float | Literal["fl", "0", "0.5", "1", "1.5", "2", "2.5", "3"]
RotationAngles = Literal[0, 90, 180, 270]
OptimalLocationEntries = Dict[Literal["x", "y"], float]


StartEndLocationTuple = Tuple[Location, Location]
PreprocessedStartEndCombinations = Dict[
    SpecificStartEndPositionsDicts,
    List[Tuple[Letter, List[MotionAttributesDicts]]],
]
OptimalLocationDicts = Dict[str, OptimalLocationEntries]
DictVariants = (
    MotionAttributesDicts | SpecificStartEndPositionsDicts | OptimalLocationDicts
)
DictVariantsLists = List[DictVariants]
PictographDataframe = Dict[Letter, List[DictVariantsLists]]


class Mode(Enum):
    TOG_SAME = "TS"
    TOG_OPPOSITE = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPPOSITE = "SO"
    QUARTER_TIME_SAME = "QTS"
    QUARTER_TIME_OPPOSITE = "QTO"


class PictographAttributesDict(TypedDict):
    start_position: PictographAttribute.START_POSITION
    end_position: PictographAttribute.END_POSITION
    letter: LETTER
    handpath_mode: PictographAttribute.HANDPATH_MODE
    motion_type_combination: PictographAttribute.MOTION_TYPE_COMBINATION


### LETTER GROUPS ###


class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class LetterGroupsByMotionType(Enum):
    ADGJMPS = "ADGJMPS"
    BEHKNQT = "BEHKNQT"
    αβΓ = "αβΓ"
    CFILORUV = "CFILORUV"
    WYΣθ = "WYΣθ"
    XZΔΩ = "XZΔΩ"
    X_Z_Δ_Ω_ = "X-Z-Δ-Ω-"
    ΦΨΛ = "ΦΨΛ"
    Φ_Ψ_Λ_ = "Φ-Ψ-Λ-"


class MotionTypeCombinationMapping(TypedDict):
    MotionTypeCombination.PRO_VS_PRO: LetterGroupsByMotionType.ADGJMPS
    MotionTypeCombination.ANTI_VS_ANTI: LetterGroupsByMotionType.BEHKNQT
    MotionTypeCombination.STATIC_VS_STATIC: LetterGroupsByMotionType.αβΓ
    MotionTypeCombination.PRO_VS_ANTI: LetterGroupsByMotionType.CFILORUV
    MotionTypeCombination.STATIC_VS_PRO: LetterGroupsByMotionType.WYΣθ
    MotionTypeCombination.STATIC_VS_ANTI: LetterGroupsByMotionType.XZΔΩ
    MotionTypeCombination.DASH_VS_PRO: LetterGroupsByMotionType.WYΣθ
    MotionTypeCombination.DASH_VS_ANTI: LetterGroupsByMotionType.X_Z_Δ_Ω_
    MotionTypeCombination.DASH_VS_STATIC: LetterGroupsByMotionType.ΦΨΛ
    MotionTypeCombination.DASH_VS_DASH: LetterGroupsByMotionType.Φ_Ψ_Λ_


ParallelCombinationsSet = Set[Tuple[str, str, str, str]]
