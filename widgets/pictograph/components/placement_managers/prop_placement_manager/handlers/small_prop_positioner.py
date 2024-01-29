from typing import TYPE_CHECKING
from .small_bilateral_prop_positioner import SmallBilateralPropPositioner
from .small_unilateral_prop_positioner import SmallUnilateralPropPositioner
if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SmallPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        if len(self.beta_prop_positioner.classifier.small_uni) == 2:
            SmallUnilateralPropPositioner(self.beta_prop_positioner).reposition(
                self.beta_prop_positioner.classifier.small_uni
            )
        elif len(self.beta_prop_positioner.classifier.small_bi) == 2:
            SmallBilateralPropPositioner(self.beta_prop_positioner).reposition()
