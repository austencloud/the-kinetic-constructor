from typing import TYPE_CHECKING
from data.constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ICON_DIR,
    OPP,
    PROP_ROT_DIR,
    SAME,
)
from Enums.MotionAttributes import PropRotDir
from Enums.Enums import VTG_Directions
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from utilities.path_helpers import get_images_and_data_path
from .vtr_dir_button import VtgDirButton

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from widgets.sequence_widget.graph_editor.adjustment_panel.turns_box.turns_box import (
        TurnsBox,
    )


class VtgDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.graph_editor = turns_box.graph_editor
        self.previous_turns = 0
        self.vtg_state = self.turns_box.vtg_dir_btn_state
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
        self.json_manager = self.graph_editor.main_widget.json_manager
        self.color = self.turns_box.color
        self.vtg_dir_buttons: list[VtgDirButton] = self._setup_vtg_dir_buttons()
        self.hide_vtg_dir_buttons()

    def show_vtg_dir_buttons(self) -> None:
        self.opp_button.show()
        self.same_button.show()

    def hide_vtg_dir_buttons(self) -> None:
        self.opp_button.hide()
        self.same_button.hide()

    def _setup_vtg_dir_buttons(self) -> list[QPushButton]:
        same_path = get_images_and_data_path(f"{ICON_DIR}same_direction.png")
        opp_path = get_images_and_data_path(f"{ICON_DIR}opp_direction.png")
        self.same_button: VtgDirButton = self.create_vtg_dir_button(
            same_path, lambda: self._set_vtg_dir(SAME), SAME
        )
        self.opp_button: VtgDirButton = self.create_vtg_dir_button(
            opp_path, lambda: self._set_vtg_dir(OPP), OPP
        )
        self.same_button.unpress()
        self.opp_button.unpress()

        return [self.same_button, self.opp_button]

    def create_vtg_dir_button(self, icon_path: str, callback, vtg_dir) -> VtgDirButton:
        button = VtgDirButton(vtg_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def _set_vtg_dir(self, vtg_dir: VTG_Directions) -> None:
        self._update_pictographs_vtg_dir(vtg_dir)
        self._update_button_states(self.vtg_dir_buttons, vtg_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VTG_Directions) -> None:
        pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        pictograph_index = self.beat_frame.get_index_of_currently_selected_beat()
        for motion in pictograph.motions.values():
            other_motion = pictograph.get.other_motion(motion)
            if motion.check.is_dash() or motion.check.is_static():
                if other_motion.check.is_shift():
                    pictograph.direction = vtg_dir
                    if vtg_dir == SAME:
                        prop_rot_dir = other_motion.prop_rot_dir
                        self._update_pictograph_prop_rot_dir_from_vtg_dir_setting(
                            motion, prop_rot_dir
                        )
                        self.json_manager.updater.update_rot_dir_in_json_at_index(
                            pictograph_index + 2, self.color, prop_rot_dir
                        )
                    elif vtg_dir == OPP:
                        prop_rot_dir = self._opposite_prop_rot_dir(
                            other_motion.prop_rot_dir
                        )
                        self._update_pictograph_prop_rot_dir_from_vtg_dir_setting(
                            motion, prop_rot_dir
                        )
                        self.json_manager.updater.update_rot_dir_in_json_at_index(
                            pictograph_index + 2, self.color, prop_rot_dir
                        )

    def _update_pictograph_prop_rot_dir_from_vtg_dir_setting(
        self, motion: "Motion", prop_rot_dir: PropRotDir
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {f"{motion.color}_attributes": {PROP_ROT_DIR: prop_rot_dir}}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self, buttons: list[VtgDirButton], active_direction: VTG_Directions
    ) -> None:
        for button in buttons:
            if button.direction == active_direction:
                button.press()
                self.vtg_state[button.direction] = True
            else:
                button.unpress()
                self.vtg_state[button.direction] = False

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDir) -> PropRotDir:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def unpress_vtg_buttons(self) -> None:
        self.same_button.unpress()
        self.opp_button.unpress()

    def resize_vtg_dir_buttons(self) -> None:
        button_size = int(self.turns_box.height() * 0.25)
        icon_size = int(button_size * 0.8)
        for button in self.vtg_dir_buttons:
            button.setFixedSize(button_size, button_size)
            button.setIconSize(QSize(icon_size, icon_size))
