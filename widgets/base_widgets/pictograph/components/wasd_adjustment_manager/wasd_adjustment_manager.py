from typing import TYPE_CHECKING

from widgets.base_widgets.pictograph.components.wasd_adjustment_manager.prop_placement_override_manager import (
    PropPlacementOverrideManager,
)


from .arrow_movement_manager import ArrowMovementManager
from .rotation_angle_override_manager import RotationAngleOverrideManager

if TYPE_CHECKING:
    from widgets.base_widgets.pictograph.base_pictograph import BasePictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph
        self.entry_remover = (
            self.pictograph.arrow_placement_manager.special_positioner.data_updater.entry_remover
        )
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_angle_override_manager = RotationAngleOverrideManager(self)
        self.prop_placement_override_manager = PropPlacementOverrideManager(self)

    def handle_special_placement_removal(self) -> None:
        if not self.pictograph.selected_arrow:
            return
        letter = self.pictograph.letter
        self.entry_remover.remove_special_placement_entry(
            letter, self.pictograph.selected_arrow
        )
        self.pictograph.updater.update_pictograph()
