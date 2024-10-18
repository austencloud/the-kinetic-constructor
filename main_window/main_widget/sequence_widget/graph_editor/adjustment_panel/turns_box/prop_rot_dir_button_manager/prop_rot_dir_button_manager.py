from typing import TYPE_CHECKING
from Enums.Enums import VTG_Directions
from PyQt6.QtGui import QIcon
from Enums.letters import Letter
from data.constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ICON_DIR,
    PROP_ROT_DIR,
)
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication
from utilities.path_helpers import get_images_and_data_path
from .prop_rot_dir_button import PropRotDirButton

if TYPE_CHECKING:
    from ..turns_box import TurnsBox
    from objects.motion.motion import Motion


class PropRotDirButtonManager:
    def __init__(self, turns_box: "TurnsBox") -> None:
        self.turns_box = turns_box
        self.previous_turns = 0
        self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons
        self.graph_editor = turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
        self.json_manager = self.graph_editor.main_widget.json_manager

    def _setup_prop_rot_dir_buttons(self) -> list[PropRotDirButton]:
        cw_path = get_images_and_data_path(f"{ICON_DIR}clock/clockwise.png")
        ccw_path = get_images_and_data_path(f"{ICON_DIR}clock/counter_clockwise.png")
        self.cw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            cw_path,
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            ccw_path,
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
            COUNTER_CLOCKWISE,
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()
        self.cw_button.hide()
        self.ccw_button.hide()
        return [self.cw_button, self.ccw_button]

    def create_prop_rot_dir_button(
        self, icon_path: str, callback, prop_rot_dir
    ) -> PropRotDirButton:
        button = PropRotDirButton(prop_rot_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def _set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        """Set the prop rotation direction and update the motion and letter."""
        # if the motion's prop_rot_dir already matches what the user selected, return
        if self.turns_box.prop_rot_dir_btn_state[prop_rot_dir]:
            return
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_pictograph
        for motion in pictograph.motions.values():
            if motion.color == self.turns_box.color:
                motion.prop_rot_dir = prop_rot_dir
                new_letter = (
                    self.graph_editor.main_widget.letter_determiner.determine_letter(
                        motion, swap_prop_rot_dir=True
                    )
                )
                self._update_pictograph_and_json(motion, new_letter)
        self._update_button_states(self.prop_rot_dir_buttons, prop_rot_dir)

    def _update_pictograph_and_json(self, motion: "Motion", new_letter: Letter) -> None:
        """Update the pictograph and JSON with the new letter and motion attributes."""
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        if new_letter:
            pictograph_dict = {
                "letter": new_letter.value,
                motion.color
                + "_attributes": {
                    "motion_type": motion.motion_type,
                    "prop_rot_dir": motion.prop_rot_dir,
                    "end_ori": motion.end_ori,
                },
            }
        else:
            pictograph_dict = {
                motion.color
                + "_attributes": {
                    "motion_type": motion.motion_type,
                    "prop_rot_dir": motion.prop_rot_dir,
                    "end_ori": motion.end_ori,
                },
            }

        motion.pictograph.updater.update_pictograph(pictograph_dict)
        motion.pictograph.view.repaint()
        GE_pictograph = (
            self.turns_box.adjustment_panel.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        GE_pictograph.view.repaint()
        QApplication.processEvents()
        json_index = pictograph_index + 2
        self.json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            json_index, motion.color, motion.prop_rot_dir
        )
        self.json_manager.updater.motion_type_updater.update_motion_type_in_json_at_index(
            json_index, motion.color, motion.motion_type
        )
        if new_letter:
            self.json_manager.updater.letter_updater.update_letter_in_json_at_index(
                json_index, new_letter.value
            )
        self.turns_box.turns_widget.motion_type_label.update_motion_type_label(
            motion.motion_type
        )

        # Running the validation engine
        self.graph_editor.main_widget.json_manager.validation_engine.run(
            is_current_sequence=True
        )

        # Triggering updates for UI components
        self.graph_editor.sequence_widget.beat_frame.updater.update_beats_from_json()
        self.graph_editor.main_widget.sequence_widget.current_word_label.set_current_word(
            self.graph_editor.sequence_widget.beat_frame.get.current_word()
        )

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: str) -> None:
        pictograph = self.turns_box.graph_editor.pictograph_container.GE_pictograph
        for motion in pictograph.motions.values():
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
        self, motion: "Motion", prop_rot_dir: str
    ) -> None:
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {
            motion.color + "_attributes": {"prop_rot_dir": prop_rot_dir},
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)
        self.json_manager.updater.update_prop_rot_dir_in_json_at_index(
            pictograph_index + 2, motion.color, prop_rot_dir
        )

    def _update_button_states(
        self,
        buttons: list[PropRotDirButton],
        prop_rot_dir: str,
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

    def _opposite_prop_rot_dir(self, prop_rot_dir: str) -> str:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def unpress_prop_rot_dir_buttons(self) -> None:
        self.cw_button.unpress()
        self.ccw_button.unpress()

    def resize_prop_rot_dir_buttons(self) -> None:
        button_size = int(self.turns_box.graph_editor.height() * 0.25)
        icon_size = int(button_size * 0.8)
        for button in self.prop_rot_dir_buttons:
            button.setFixedSize(button_size, button_size)
            button.setIconSize(QSize(icon_size, icon_size))
