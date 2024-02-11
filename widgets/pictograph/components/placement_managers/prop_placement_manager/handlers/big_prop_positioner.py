from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class BigPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.ppm = beta_prop_positioner.prop_placement_manager
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        if self.pictograph.check.ends_with_non_hybrid_ori():
            for prop in self.beta_prop_positioner.classifier.big_props:
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
            for prop in self.beta_prop_positioner.classifier.big_props:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)
