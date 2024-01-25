from typing import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from ..turns_tuple_generator import TurnsTupleGenerator
from .handlers.motion_attr_key_generator import MotionAttrKeyGenerator
from .handlers.special_placement_data_updater import SpecialPlacementDataUpdater

if TYPE_CHECKING:
    from ...arrow_placement_manager import ArrowPlacementManager
    from widgets.pictograph.pictograph import Pictograph


class SpecialArrowPositioner:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.pictograph: Pictograph = placement_manager.pictograph
        self.data_loader = (self)

        self.data_updater = SpecialPlacementDataUpdater(self)
        self.motion_key_generator = MotionAttrKeyGenerator(self)
        self.turns_tuple_generator = TurnsTupleGenerator(self)

