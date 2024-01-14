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
from .base_ig_turns_widget import BaseIGTurnsWidget

if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseIGTurnsWidget):
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

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        simulate_same_click = False

        # Check if any static motion with zero turns exists
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if (
                    motion.motion_type in [DASH, STATIC]
                    and motion.turns == 0
                    and motion.motion_type == self.attr_box.motion_type
                ):
                    simulate_same_click = True
                    break
            if simulate_same_click:
                break

        # Simulate CW button click if necessary
        if simulate_same_click:
            if hasattr(self.attr_box.header_widget, "same_button"):
                if (
                    not self.attr_box.same_button.isChecked()
                    and not self.attr_box.opp_button.isChecked()
                ):
                    self._simulate_same_button_click()
                # set the stylesheet to pressed
                self.attr_box.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=True)
                )

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                    other_motion = pictograph.motions[
                        RED if motion.color == BLUE else BLUE
                    ]
                    if hasattr(self.attr_box.header_widget, "same_button"):
                        if self.attr_box.same_button.isChecked():
                            if other_motion.prop_rot_dir:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.attr_box.opp_button.isChecked():
                            if other_motion.prop_rot_dir is CLOCKWISE:
                                motion.prop_rot_dir = COUNTER_CLOCKWISE
                            elif other_motion.prop_rot_dir is COUNTER_CLOCKWISE:
                                motion.prop_rot_dir = CLOCKWISE

        self.adjust_turns(adjustment)

    def _simulate_same_button_click(self) -> None:
        self.attr_box.same_button.setChecked(True)
        self.attr_box.opp_button.setChecked(False)
        self.attr_box.same_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=True)
        )
        self.attr_box.opp_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
        )

    def _set_turns(self, new_turns: int | float) -> None:
        self._direct_set_turns(new_turns)
