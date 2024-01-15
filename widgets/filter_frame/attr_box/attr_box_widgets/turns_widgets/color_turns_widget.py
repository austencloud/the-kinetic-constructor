from typing import TYPE_CHECKING
from .base_turns_widget.base_turns_widget import BaseTurnsWidget

if TYPE_CHECKING:
    from ...color_attr_box import ColorAttrBox


class ColorTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "ColorAttrBox") -> None:
        """Initialize the IGColorTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box

        self.attr_box.same_button = self.attr_box.vtg_dir_widget.same_button
        self.opp_btn = self.attr_box.vtg_dir_widget.opp_button
        self.same_opp_buttons = [self.attr_box.same_button, self.opp_btn]
        self.color = self.attr_box.color
        self.pictographs = self.attr_box.pictographs


    ### EVENT HANDLERS ###

    def resize_turns_widget(self) -> None:
        self.turn_display_manager.update_turnbox_size()
        self.turn_display_manager.update_adjust_turns_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on color."""
        for pictograph in self.attr_box.pictographs.values():
            self.turn_adjustment_manager._adjust_turns_for_pictograph(
                pictograph, adjustment
            )
