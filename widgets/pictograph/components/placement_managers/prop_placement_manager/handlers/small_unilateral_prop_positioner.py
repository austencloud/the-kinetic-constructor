from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class SmallUnilateralPropPositioner:
    def __init__(self, beta_positioner: "BetaPropPositioner") -> None:
        self.beta_positioner = beta_positioner
        self.prop_placement_manager = beta_positioner.prop_placement_manager
        self.pictograph = beta_positioner.pictograph
        self.dir_calculator = self.prop_placement_manager.dir_calculator
        self.blue_prop = self.pictograph.blue_prop
        self.red_prop = self.pictograph.red_prop
        self.red_motion = self.pictograph.red_motion
        self.blue_motion = self.pictograph.blue_motion
        self.default_positioner = self.prop_placement_manager.default_positioner
        self.classifier = self.beta_positioner.classifier

    def reposition(self) -> None:
        for prop in self.classifier.small_uni:
            self.default_positioner.set_prop_to_default_loc(prop)
            if self.classifier.small_uni[0].ori == self.classifier.small_uni[1].ori:
                red_direction = self.dir_calculator.get_dir(self.red_motion)
                blue_direction = self.dir_calculator.get_dir(self.blue_motion)
                self.beta_positioner.move_prop(self.red_prop, red_direction)
                self.beta_positioner.move_prop(self.blue_prop, blue_direction)
