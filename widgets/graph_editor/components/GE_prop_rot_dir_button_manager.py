from typing import TYPE_CHECKING
from Enums.Enums import VTG_Directions

from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    PROP_ROT_DIR,
    STATIC,
)
from Enums.MotionAttributes import (
    PropRotDir,
)
from PyQt6.QtCore import QSize


from path_helpers import get_images_and_data_path
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
            self.turns_box.adjustment_panel.graph_editor.main_widget.button_factory
        )
        cw_path = get_images_and_data_path(f"{ICON_DIR}clock/clockwise.png")
        ccw_path = get_images_and_data_path(f"{ICON_DIR}clock/counter_clockwise.png")
        self.cw_button: PropRotDirButton = button_factory.create_prop_rot_dir_button(
            cw_path,
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = button_factory.create_prop_rot_dir_button(
            ccw_path,
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
            motion.color + "_" + PROP_ROT_DIR: prop_rot_dir,
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
        button_size = int(self.turns_box.height() * 0.25)
        icon_size = int(button_size * 0.8)
        for button in self.prop_rot_dir_buttons:
            button.setFixedSize(button_size, button_size)
            button.setIconSize(QSize(icon_size, icon_size))
