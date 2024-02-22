from typing import TYPE_CHECKING
from Enums.Enums import VTG_Directions

from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    OPP,
    PROP_ROT_DIR,
    SAME,
    STATIC,
)
from Enums.MotionAttributes import (
    Color,
    PropRotDir,
)
from PyQt6.QtCore import QSize


from widgets.factories.button_factory.buttons.rot_dir_buttons import (
    PropRotDirButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import GE_TurnsBox
    from objects.motion.motion import Motion


class GE_PropRotDirButtonManager:
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        self.turns_box = turns_box
        self.previous_turns = 0
        self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons

    def _setup_prop_rot_dir_buttons(self) -> list[PropRotDirButton]:
        button_factory = (
            self.turns_box.turns_panel.graph_editor.main_widget.button_factory
        )
        self.cw_button: PropRotDirButton = button_factory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/clockwise.png",
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = button_factory.create_prop_rot_dir_button(
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
        pictograph = self.turns_box.graph_editor.GE_pictograph
        for motion in pictograph.motions.values():
            other_motion = pictograph.motions[
                Color.RED if motion.color == Color.BLUE else Color.BLUE
            ]
            if motion.check.is_dash() or motion.check.is_static():
                if other_motion.check.is_shift():
                    if motion.color == self.turns_box.color:
                        if vtg_dir == SAME:
                            self._update_pictograph_vtg_dir(
                                motion, other_motion.prop_rot_dir
                            )
                        elif vtg_dir == OPP:
                            self._update_pictograph_vtg_dir(
                                motion,
                                self._opposite_prop_rot_dir(other_motion.prop_rot_dir),
                            )

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> None:
        pictograph = self.turns_box.graph_editor.GE_pictograph
        for motion in pictograph.motions.values():
            if motion.motion_type in [DASH, STATIC]:
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
            motion.color.value + "_" + PROP_ROT_DIR: prop_rot_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self,
        buttons: list[PropRotDirButton],
        prop_rot_dir: PropRotDir,
    ) -> None:
        for button in buttons:
            if button.prop_rot_dir == prop_rot_dir:
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

    def resize_prop_rot_dir_buttons(self) -> None:
        header_height = self.turns_box.header_widget.header_label.height()
        for button in self.prop_rot_dir_buttons:
            button_height = header_height
            button_width = button_height 
            button.setFixedSize(button_width, button_height)
            icon_size = int(button_height * 0.8)
            button.setIconSize(QSize(icon_size, icon_size))
