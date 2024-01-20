from typing import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from ..turns_tuple_generator import TurnsTupleGenerator
from .handlers.adjustment_calculator import AdjustmentCalculator
from .handlers.adjustment_mapper import AdjustmentMapper
from .handlers.data_sorter import DataSorter
from .handlers.motion_attr_key_generator import MotionAttrKeyGenerator
from .handlers.rot_angle_override_handler import RotAngleOverrideHandler
from .handlers.special_placement_data_loader import SpecialPlacementDataLoader
from .handlers.special_placement_data_updater import SpecialPlacementDataUpdater

if TYPE_CHECKING:
    from ...arrow_placement_manager import ArrowPlacementManager
    from widgets.pictograph.pictograph import Pictograph


class SpecialArrowPositioner:
    """
    Manages the special positioning of arrows whose default positions
    are not optimal due to the placement of other graphical objects.

    Attributes:
        pictograph (Pictograph): The associated pictograph.
        special_placements (Dict): Loaded special placement rules.
        data_loader (SpecialPlacementDataLoader): Loads the json data.
        data_updater (SpecialPlacementDataUpdater): Updates the json data.
        adjustment_calculator (AdjustmentCalculator): Calculates adjustments.
        key_generator (KeyGenerator): Generates adjustment keys.
        rot_angle_handler (RotAngleOverrideHandler): Overrides rot angles from json.
        data_sorter (DataSorter): Sorts the json data.
        adjustment_mapper (AdjustmentMapper): Maps adjustments to arrows.
    """

    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.pictograph: Pictograph = placement_manager.pictograph
        self.data_loader = SpecialPlacementDataLoader(self)
        self.special_placements = self.data_loader.load_placements()

        self.data_updater = SpecialPlacementDataUpdater(self)
        self.adjustment_calculator = AdjustmentCalculator(self)
        self.rot_angle_handler = RotAngleOverrideHandler(self)
        self.adjustment_mapper = AdjustmentMapper(self)
        self.motion_key_generator = MotionAttrKeyGenerator(self)
        self.turns_tuple_generator = TurnsTupleGenerator(self)
        self.data_sorter = DataSorter(self)

    def update_arrow_placement(self, arrow: Arrow) -> None:
        adjustment_key = self.turns_tuple_generator.generate_turns_tuple(
            arrow.scene.letter
        )
        adjustment = self.adjustment_mapper.apply_adjustment_to_arrow(arrow)
        if adjustment:
            self.data_updater.update_specific_entry_in_json(
                self.pictograph.letter, adjustment_key, adjustment
            )
