from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SmallUnilateralPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.ppm = beta_prop_positioner.ppm
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        if (
            self.beta_prop_positioner.classifier.small_uni[0].ori
            == self.beta_prop_positioner.classifier.small_uni[1].ori
        ):
            for prop in self.beta_prop_positioner.classifier.small_uni:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)
                red_direction = self.ppm.dir_calculator.get_dir(
                    self.pictograph.red_motion
                )
                blue_direction = self.ppm.dir_calculator.get_dir(
                    self.pictograph.blue_motion
                )
                self.beta_prop_positioner.move_prop(
                    self.pictograph.red_prop, red_direction
                )
                self.beta_prop_positioner.move_prop(
                    self.pictograph.blue_prop, blue_direction
                )
        else:
            for prop in self.beta_prop_positioner.classifier.small_uni:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)
