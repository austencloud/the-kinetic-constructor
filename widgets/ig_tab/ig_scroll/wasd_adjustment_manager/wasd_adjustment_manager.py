from .adjustment_persistence_manager import AdjustmentPersistenceManager
from .arrow_movement_manager import ArrowMovementManager
from .letter_adjustment_handler import (
    LetterAdjustmentHandlerFactory,
    NonHybridLetterHandler,
    Type1HybridLetterHandler,
    Type2LetterHandler,
)
from .rotation_angle_manager import RotationAngleManager
from .turn_adjustment_manager import TurnAdjustmentManager
from utilities.TypeChecking.Letters import (
    non_hybrid_letters,
    Type1_hybrid_letters,
    Type2_letters,
)

class WASD_AdjustmentManager:
    def __init__(self, pictograph) -> None:
        self.turn_manager = TurnAdjustmentManager(pictograph)
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_manager = RotationAngleManager(pictograph)
        self.persistence_manager = AdjustmentPersistenceManager(pictograph)
        self.pictograph = pictograph
        handler_map = {
            **{letter: NonHybridLetterHandler for letter in non_hybrid_letters},
            **{letter: Type1HybridLetterHandler for letter in Type1_hybrid_letters},
            **{letter: Type2LetterHandler for letter in Type2_letters},
        }
        self.handler_factory = LetterAdjustmentHandlerFactory(handler_map)

