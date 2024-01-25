from typing import TYPE_CHECKING, List, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    MOTION_TYPE,
    OPP,
    PROP_ROT_DIR,
    RED,
    SAME,
    STATIC,
    Type4,
    Type5,
    Type6,
)
from utilities.TypeChecking.MotionAttributes import PropRotDirs
from utilities.TypeChecking.TypeChecking import VtgDirections
from widgets.factories.button_factory.button_factory import ButtonFactory
from ...factories.button_factory.buttons.rot_dir_buttons import (
    VtgDirButton,
    PropRotDirButton,
)

from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from widgets.turns_box.turns_box import TurnsBox
    from objects.motion.motion import Motion


class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.previous_turns = 0
        self.prop_rot_dir_buttons: List[
            PropRotDirButton
        ] = self._setup_prop_rot_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/clockwise.png",
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
            COUNTER_CLOCKWISE,
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()
        self.cw_button.hide()
        self.ccw_button.hide()
        return [self.cw_button, self.ccw_button]

    def _set_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        self._update_pictographs_prop_rot_dir(prop_rot_dir)
        self._update_button_states(self.prop_rot_dir_buttons, prop_rot_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        for (
            pictograph
        ) in (
            self.turns_box.turns_panel.filter_tab.section.scroll_area.pictographs.values()
        ):
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[RED if motion.color == BLUE else BLUE]
                if motion.check.is_dash() or motion.check.is_static():
                    if other_motion.check.is_shift():
                        if motion.motion_type == self.turns_box.motion_type:
                            if vtg_dir == SAME:
                                self._update_pictograph_vtg_dir(
                                    motion, other_motion.prop_rot_dir
                                )
                            elif vtg_dir == OPP:
                                self._update_pictograph_vtg_dir(
                                    motion,
                                    self._opposite_prop_rot_dir(
                                        other_motion.prop_rot_dir
                                    ),
                                )

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        for (
            pictograph
        ) in (
            self.turns_box.turns_panel.filter_tab.section.scroll_area.pictographs.values()
        ):
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if self.turns_box.attribute_type == MOTION_TYPE:
                        if motion.motion_type == self.turns_box.motion_type:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)
                    elif self.turns_box.attribute_type == COLOR:
                        if motion.color == self.turns_box.color:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)

    def _update_pictograph_vtg_dir(
        self, motion: "Motion", vtg_dir: VtgDirections
    ) -> None:
        motion.prop_rot_dir = vtg_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: vtg_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_pictograph_prop_rot_dir(
        self, motion: "Motion", prop_rot_dir: PropRotDirs
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: prop_rot_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self,
        buttons: List[Union[PropRotDirButton, VtgDirButton]],
        active_direction: VtgDirections,
    ) -> None:
        for button in buttons:
            if button.prop_rot_dir == active_direction:
                button.press()
                self.turns_box.prop_rot_dir_btn_state[button.prop_rot_dir] = True
            else:
                button.unpress()
                self.turns_box.prop_rot_dir_btn_state[button.prop_rot_dir] = False

    def show_prop_rot_dir_buttons(self) -> None:
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        for button in self.prop_rot_dir_buttons:
            button.hide()

        
    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> PropRotDirs:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.unpress()
        self.ccw_button.unpress()

    def update_visibility_based_on_motion(self, letter_type, new_turns, attribute_value) -> None:
        if self.turns_box.turns_panel.filter_tab.section.letter_type in [
            Type4,
            Type5,
            Type6,
        ]:
            if new_turns > 0:
                if self.previous_turns == 0:
                    self.show_prop_rot_dir_buttons()
            elif new_turns == 0:
                self.previous_turns = 0
                self.hide_prop_rot_dir_buttons()
