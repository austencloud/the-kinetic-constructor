from constants.string_constants import COLOR
from typing import TYPE_CHECKING
from objects.arrow.arrow import Arrow
from objects.motion import Motion

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from utilities.TypeChecking.TypeChecking import ArrowAttributesDicts


class GhostArrow(Arrow):
    """
    Represents a ghost arrow object, displaying the position that an arrow will be while dragging if the user were to drop it.

    Inherits from the Arrow class.

    Attributes:
        pictograph (Pictograph): The pictograph object.
        color (str): The color of the arrow.
        target_arrow (Arrow): The arrow that the ghost arrow is copying.

    Methods:
        __init__: Initialize a GhostArrow object.

    """

    def __init__(
        self,
        pictograph: "Pictograph",
        attributes: "ArrowAttributesDicts",
        motion: "Motion",
    ) -> None:
        super().__init__(pictograph, attributes, motion)
        self.setOpacity(0.2)
        self.pictograph = pictograph
        self.color = attributes[COLOR]
        self.target_arrow: "Arrow" = None

    def update_ghost_arrow(self, attributes) -> None:
        self.update_attributes(attributes)
        self.update_appearance()
        self.show()
