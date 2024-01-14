from typing import TYPE_CHECKING
from constants import (
    DASH,
    NO_ROT,
    STATIC,
)
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

    def _update_turns_directly_by_color(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self.turn_direct_set_manager._directly_set_turns(turns)

    def _update_pictographs_turns_by_color(self, new_turns) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.color == self.attr_box.color:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self.attr_box.vtg_dir_widget._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self.attr_box.vtg_dir_widget._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)


    def _update_pictographs_turns_by_color(self, new_turns) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.color == self.attr_box.color:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self.attr_box.vtg_dir_widget._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self.attr_box.vtg_dir_widget._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    ### EVENT HANDLERS ###

    def resize_turns_widget(self) -> None:
        self.turn_display_manager.update_turnbox_size()
        self.turn_display_manager.update_adjust_turns_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on color."""
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_manager._adjust_turns_for_pictograph(
                pictograph, adjustment
            )


