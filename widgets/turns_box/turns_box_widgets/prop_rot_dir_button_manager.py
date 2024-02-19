from typing import TYPE_CHECKING, Union
from Enums.Enums import LetterType, VTG_Directions

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
)
from Enums.MotionAttributes import (
    Color,
    LeadStates,
    MotionType,
    PropRotDir,
)
from widgets.factories.button_factory.button_factory import ButtonFactory
from ...factories.button_factory.buttons.rot_dir_buttons import (
    VtgDirButton,
    PropRotDirButton,
)

from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from widgets.turns_box.codex_turns_box import CodexTurnsBox
    from objects.motion.motion import Motion


class PropRotDirButtonManager:
    def __init__(self, turns_box: "CodexTurnsBox") -> None:
        self.turns_box = turns_box
        self.previous_turns = 0
        self.prop_rot_dir_buttons: list[PropRotDirButton] = (
            self._setup_prop_rot_dir_buttons()
        )
        self.buttons = self.prop_rot_dir_buttons

    def _setup_prop_rot_dir_buttons(self) -> list[QPushButton]:
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

    def _set_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> None:
        self._update_pictographs_prop_rot_dir(prop_rot_dir)
        self._update_button_states(self.prop_rot_dir_buttons, prop_rot_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VTG_Directions) -> None:
        for (
            pictograph
        ) in (
            self.turns_box.turns_panel.turns_tab.section.scroll_area.pictograph_cache.values()
        ):
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[
                    Color.RED if motion.color == Color.BLUE else Color.BLUE
                ]
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

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> None:
        for (
            pictograph
        ) in (
            self.turns_box.turns_panel.turns_tab.section.scroll_area.pictograph_cache.values()
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
        self, motion: "Motion", vtg_dir: VTG_Directions
    ) -> None:
        motion.prop_rot_dir = vtg_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: vtg_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_pictograph_prop_rot_dir(
        self, motion: "Motion", prop_rot_dir: PropRotDir
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: prop_rot_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self,
        buttons: list[Union[PropRotDirButton, VtgDirButton]],
        active_direction: VTG_Directions,
    ) -> None:
        for button in buttons:
            if button.prop_rot_dir == active_direction:
                button.press()
                button.update_state_dict(self.turns_box.prop_rot_dir_btn_state, True)
            else:
                button.unpress()
                button.update_state_dict(self.turns_box.prop_rot_dir_btn_state, False)

    def show_prop_rot_dir_buttons(self) -> None:
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self) -> None:
        for button in self.prop_rot_dir_buttons:
            button.hide()

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> PropRotDir:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.unpress()
        self.ccw_button.unpress()

    def update_visibility_based_on_motion(
        self, new_turns, attribute_value: Union[Color, MotionType, LeadStates]
    ) -> None:
        if self.turns_box.turns_panel.turns_tab.section.letter_type in [
            LetterType.Type4,
            LetterType.Type5,
            LetterType.Type6,
        ]:
            if new_turns > 0:
                if self.previous_turns == 0:
                    self.show_prop_rot_dir_buttons()
            elif new_turns == 0:
                self.previous_turns = 0
                self.hide_prop_rot_dir_buttons()
