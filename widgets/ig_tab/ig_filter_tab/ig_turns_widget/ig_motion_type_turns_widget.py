from typing import TYPE_CHECKING
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    RED,
    STATIC,
)
from objects.pictograph.pictograph import Pictograph
from widgets.attr_box_widgets.base_turns_widget import BaseTurnsWidget

if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGMotionTypeAttrBox") -> None:
        """Initialize the IGMotionTypeTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box

    def update_turns_display_for_pictograph(self, pictograph: Pictograph) -> None:
        """Update the turnbox display based on the latest turns value of the pictograph."""
        for motion in pictograph.get_motions_by_type(self.attr_box.motion_type):
            self.update_turns_display(motion.turns)
            break

    def _update_turns_directly_by_motion_type(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._direct_set_turns(turns)

    def resize_turns_widget(self) -> None:
        self.update_turnbox_size()
        self.update_adjust_turns_button_size()


    def _set_turns(self, new_turns: int | float) -> None:
        self._direct_set_turns(new_turns)
