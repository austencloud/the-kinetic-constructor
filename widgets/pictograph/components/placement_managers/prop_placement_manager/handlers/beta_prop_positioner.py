from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from objects.prop.prop import Prop
from Enums.Enums import Directions
from .big_prop_positioner import BigPropPositioner
from .prop_classifier import PropClassifier
from .reposition_beta_props_by_letter_manager import RepositionBetaByLetterHandler
from .small_prop_positioner import SmallPropPositioner
from .swap_beta_handler import SwapBetaHandler

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from ..prop_placement_manager import PropPlacementManager


class BetaPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph: "Pictograph" = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager

        self.classifier = PropClassifier(self.pictograph)
        self.hand_positioner = HandPositioner(self)
        self.small_prop_positioner = SmallPropPositioner(self)
        self.big_prop_positioner = BigPropPositioner(self)
        self.reposition_beta_by_letter_handler = RepositionBetaByLetterHandler(self)
        self.swap_beta_handler = SwapBetaHandler(self)

    def reposition_beta_props(self) -> None:
        if self.pictograph.prop_type == PropType.Hand:
            self.hand_positioner.reposition_beta_hands()
            return
        else:
            self.classifier.classify_props()
            if len(self.classifier.big_props) == 2:
                self.big_prop_positioner.reposition()
            elif len(self.classifier.small_props) == 2:
                self.small_prop_positioner.reposition()
                self.swap_beta_handler.swap_beta_if_needed()
            elif self.classifier.hands:
                self.hand_positioner.reposition_beta_hands()
                self.swap_beta_handler.swap_beta_if_needed()

    def move_prop(self, prop: Prop, direction: Directions) -> None:
        offset_calculator = self.prop_placement_manager.offset_calculator
        offset = offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)


class HandPositioner:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph

    def reposition_beta_hands(self) -> None:
        red_hand = self.pictograph.red_prop
        blue_hand = self.pictograph.blue_prop
        self.move_hand(red_hand, "right")
        self.move_hand(blue_hand, "left")

    def move_hand(self, prop: Prop, direction: Directions) -> None:
        offset = self.beta_prop_positioner.prop_placement_manager.offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
