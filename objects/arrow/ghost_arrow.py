from typing import TYPE_CHECKING
from constants import COLOR
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class GhostArrow(Arrow):
    def __init__(self, pictograph: "Pictograph", arrow_dict) -> None:
        super().__init__(pictograph, arrow_dict)
        self.setOpacity(0.2)
        self.pictograph = pictograph
        self.color = arrow_dict[COLOR]
        self.target_arrow: "Arrow" = None
        self.is_ghost = True
