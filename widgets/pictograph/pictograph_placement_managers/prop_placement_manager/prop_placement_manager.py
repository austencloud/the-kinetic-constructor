from typing import TYPE_CHECKING
from .handlers.beta_prop_direction_calculator import BetaPropDirectionCalculator
from .handlers.beta_prop_positioner import BetaPropPositioner
from .handlers.default_prop_positioner import DefaultPropPositioner
from .handlers.prop_offset_calculator import PropOffsetCalculator

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PropPlacementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultPropPositioner(self)
        self.beta_positioner = BetaPropPositioner(self)

        self.offset_calculator = PropOffsetCalculator(self)
        self.dir_calculator = BetaPropDirectionCalculator(self)

    def update_prop_positions(self) -> None:
        for prop in self.pictograph.props.values():
            self.default_positioner.set_prop_to_default_loc(prop)
            self.default_positioner.set_prop_to_default_loc(prop.ghost)

        if self.pictograph.check.has_props_in_beta():
            self.beta_positioner.reposition_beta_props()
