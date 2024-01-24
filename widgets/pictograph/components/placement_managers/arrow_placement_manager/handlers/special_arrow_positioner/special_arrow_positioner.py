from typing import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from ..turns_tuple_generator import TurnsTupleGenerator
from .handlers.adjustment_mapper import AdjustmentMapper
from .handlers.motion_attr_key_generator import MotionAttrKeyGenerator
from .handlers.special_placement_data_updater import SpecialPlacementDataUpdater

if TYPE_CHECKING:
    from ...arrow_placement_manager import ArrowPlacementManager
    from widgets.pictograph.pictograph import Pictograph


class SpecialArrowPositioner:
    """
    Manages the special positioning of arrows whose default positions
    are not optimal due to the placement of other graphical objects.

    Attributes:
        pictograph (Pictograph): The pictograph whose arrows are being positioned.
        placement_manager (ArrowPlacementManager): The placement manager that
            is using this positioner.
        data_loader (SpecialPlacementDataLoader): The data loader that loads
            the special placement data for the pictograph.
        data_updater (SpecialPlacementDataUpdater): The data updater that
            updates the special placement data for the pictograph.
        adjustment_mapper (AdjustmentMapper): Maps the adjustment key to the
            adjustment value.
        motion_key_generator (MotionAttrKeyGenerator): Generates the motion
            attribute key for the arrow.
        turns_tuple_generator (TurnsTupleGenerator): Generates the turns tuple
            for the arrow.
            
    """

    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.pictograph: Pictograph = placement_manager.pictograph
        self.data_loader = (self)

        self.data_updater = SpecialPlacementDataUpdater(self)
        self.adjustment_mapper = AdjustmentMapper(self)
        self.motion_key_generator = MotionAttrKeyGenerator(self)
        self.turns_tuple_generator = TurnsTupleGenerator(self)

    def update_arrow_placement(self, arrow: Arrow) -> None:
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
            arrow.scene.letter
        )
        adjustment = self.adjustment_mapper.apply_adjustment_to_arrow(arrow)
        if adjustment:
            self.data_updater.update_specific_entry_in_json(
                self.pictograph.letter, turns_tuple, adjustment
            )
