from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )


class SmallBilateralPropPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.ppm = beta_prop_positioner.ppm
        self.pictograph = beta_prop_positioner.pictograph

    def reposition(self) -> None:
        if self.pictograph.check.has_hybrid_orientations():
            for prop in self.pictograph.props.values():
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

        else:
            if self.pictograph.letter in ["G", "H"]:
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_G_H()
            elif self.pictograph.letter == "I":
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_I()
            elif self.pictograph.letter in ["J", "K", "L"]:
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_J_K_L()
            elif self.pictograph.letter in ["Y", "Z"]:
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_Y_Z()
            elif self.pictograph.letter == "β":
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_β()
            elif self.pictograph.letter in ["Y-", "Z-"]:
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_Y_dash_Z_dash()
            elif self.pictograph.letter == "Ψ":
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_Ψ()
            elif self.pictograph.letter == "Ψ-":
                self.beta_prop_positioner.reposition_beta_props_by_letter_manager.reposition_Ψ_dash()
