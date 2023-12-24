from Enums import PropAttribute, PropAttributesDicts
from constants.string_constants import COLOR
from objects.motion import Motion
from objects.prop.prop import Prop

from utilities.TypeChecking.TypeChecking import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class GhostProp(Prop):
    """Represents a ghost prop object, displaying the position that a prop will be while dragging if the user were to drop it."""

    def __init__(
        self,
        pictograph: "Pictograph",
        attributes: PropAttributesDicts,
        motion: "Motion",
    ) -> None:
        super().__init__(pictograph, attributes, motion)
        self.setOpacity(0.2)
        self.pictograph = pictograph
        self.color = attributes[COLOR]
        self.target_prop: "Prop" = None
        self.setup_svg_renderer(self.svg_file)
