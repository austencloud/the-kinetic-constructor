from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    OPP,
    SAME,
    STATIC,
)
from objects.pictograph.pictograph import Pictograph
from widgets.ig_tab.ig_filter_tab.ig_turns_widget.base_ig_turns_widget import (
    BaseIGTurnsWidget,
)

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_box import IGColorAttrBox


class IGColorTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGColorAttrBox") -> None:
        """Initialize the IGColorTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.dash_button_state = {SAME: True, OPP: False}
        self.static_button_state = {SAME: True, OPP: False}
        
        self.same_button = self.attr_box.vtg_dir_widget.same_button
        self.opp_button = self.attr_box.vtg_dir_widget.opp_button
        self.same_opp_buttons = [self.same_button, self.opp_button]
        self.color = self.attr_box.color
        self.pictographs = self.attr_box.pictographs


    def _update_turns_directly_by_color(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._direct_set_turns_by_color(turns)

    def _direct_set_turns_by_color(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)
        if self.attr_box.motion_type in [DASH, STATIC]:
            if new_turns == 0:
                # Save the state before deselecting buttons
                if self.attr_box.motion_type == DASH:
                    self.dash_button_state[SAME] = self.same_button.isChecked()
                    self.dash_button_state[OPP] = self.opp_button.isChecked()
                elif self.attr_box.motion_type == STATIC:
                    self.static_button_state[SAME] = self.same_button.isChecked()
                    self.static_button_state[OPP] = self.opp_button.isChecked()

                # Deselect buttons
                self.same_button.setChecked(False)
                self.opp_button.setChecked(False)
                self.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_button_style(pressed=False)
                )
                self.opp_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_button_style(pressed=False)
                )

            elif new_turns > 0:
                if self.attr_box.motion_type == DASH and not (
                    self.dash_button_state[SAME] or self.dash_button_state[OPP]
                ):
                    # self.same_button.setChecked(True)
                    self.opp_button.setChecked(False)
                    self.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=True
                        )
                    )
                elif self.attr_box.motion_type == STATIC and not (
                    self.static_button_state[SAME] or self.static_button_state[OPP]
                ):
                    self.same_button.setChecked(True)
                else:
                    # Apply the saved state
                    self.same_button.setChecked(
                        self.dash_button_state[SAME]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[SAME]
                    )
                    self.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=(
                                self.dash_button_state[SAME]
                                if self.attr_box.motion_type == DASH
                                else self.static_button_state[SAME]
                            )
                        )
                    )
                    self.opp_button.setChecked(
                        self.dash_button_state[OPP]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[OPP]
                    )
                    self.opp_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=(
                                self.dash_button_state[OPP]
                                if self.attr_box.motion_type == DASH
                                else self.static_button_state[OPP]
                            )
                        )
                    )

        # Apply new turns to motions
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[RED if motion.color == BLUE else BLUE]

                if motion.motion_type == self.attr_box.motion_type:
                    if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
                        motion.prop_rot_dir = NO_ROT
                    if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                        if self.same_button.isChecked():
                            motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.opp_button.isChecked():
                            if other_motion.prop_rot_dir is CLOCKWISE:
                                motion.prop_rot_dir = COUNTER_CLOCKWISE
                            elif other_motion.prop_rot_dir is COUNTER_CLOCKWISE:
                                motion.prop_rot_dir = CLOCKWISE
                    pictograph_dict = {
                        f"{motion.color}_turns": new_turns,
                    }
                    pictograph.update_pictograph(pictograph_dict)


    def _update_pictographs_turns_by_color(self, new_turns):
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

    def adjust_turns_incrementally_by_color(self, adjustment) -> None:
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns(pictograph, adjustment)

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
        self.update_turnbox_size()
        self.update_adjust_turns_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on color."""
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns(pictograph, adjustment)

    def _adjust_turns_callback(self, adjustment: float) -> None:
        self.adjust_turns_incrementally_by_color(adjustment)

    def _simulate_same_button_click(self) -> None:
        self.attr_box.vtg_dir_widget.same_button.setChecked(True)
        self.attr_box.vtg_dir_widget.same_button.click()

    def _set_turns(self, new_turns: int | float) -> None:
        self._set_turns_by_color(new_turns)

    def _simulate_same_button_click(self) -> None:
        self.attr_box.same_button.setChecked(True)
        self.attr_box.opp_button.setChecked(False)
        self.attr_box.same_button.setStyleSheet(
            self.attr_box.vtg_dir_widget.get_vtg_dir_button_style(pressed=True)
        )
        self.attr_box.opp_button.setStyleSheet(
            self.attr_box.vtg_dir_widget.get_vtg_dir_button_style(pressed=False)
        )
