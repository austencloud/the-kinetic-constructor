from typing import TYPE_CHECKING
from .handlers.beta_prop_direction_calculator import BetaPropDirectionCalculator
from .handlers.beta_prop_positioner import BetaPropPositioner
from .handlers.default_prop_positioner import DefaultPropPositioner
from .handlers.prop_offset_calculator import BetaOffsetCalculator

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PropPlacementManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultPropPositioner(self)
        self.beta_positioner = BetaPropPositioner(self)

    def update_prop_positions(self, grid_mode: str = None) -> None:
        for prop in self.pictograph.props.values():
            self.default_positioner.set_prop_to_default_loc(prop, grid_mode)

        if self.pictograph.check.ends_with_beta():
            self.beta_positioner.reposition_beta_props()
