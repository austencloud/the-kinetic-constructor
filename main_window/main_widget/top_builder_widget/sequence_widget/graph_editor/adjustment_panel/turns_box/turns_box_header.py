from PyQt6.QtWidgets import (
    QApplication,
)
from typing import TYPE_CHECKING

from Enums.letters import LetterType
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE
from ..base_adjustment_box_header_widget import BaseAdjustmentBoxHeaderWidget

if TYPE_CHECKING:
    from widgets.graph_editor.adjustment_panel.turns_box.turns_box import TurnsBox


class TurnsBoxHeader(BaseAdjustmentBoxHeaderWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.adjustment_panel.graph_editor
        self.main_widget = self.graph_editor.main_widget
        self._add_widgets()
        self.update_turns_box_header()

    def update_turns_box_header(self) -> None:
        """This is called every time the GE pictograph scene is updated in order to display the correct buttons."""
        pictograph = (
            self.turns_box.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )
        letter_type = None
        motion = pictograph.get.motion_by_color(self.turns_box.color)
        turns = motion.turns
        is_shift = motion.check.is_shift()
        prop_rot_dir_button_mngr = self.turns_box.prop_rot_dir_button_manager
        vtg_dir_button_mngr = self.turns_box.vtg_dir_button_manager
        if pictograph.letter:
            letter_type = LetterType.get_letter_type(pictograph.letter)
        if letter_type == LetterType.Type1 or letter_type == None:
            self.turns_box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
            self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()
        else:
            if letter_type == LetterType.Type2 or letter_type == LetterType.Type3:
                prop_rot_dir_button_mngr.hide_prop_rot_dir_buttons()
                if turns and not is_shift:
                    self.turns_box.vtg_dir_button_manager.show_vtg_dir_buttons()
                    if pictograph.red_motion.turns or pictograph.blue_motion.turns:
                        if (
                            pictograph.red_motion.prop_rot_dir
                            == pictograph.blue_motion.prop_rot_dir
                        ):
                            self.turns_box.vtg_dir_button_manager.same_button.press()
                        else:
                            self.turns_box.vtg_dir_button_manager.opp_button.press()
                else:
                    self.turns_box.vtg_dir_button_manager.hide_vtg_dir_buttons()
            else:
                vtg_dir_button_mngr.hide_vtg_dir_buttons()

                if turns:
                    prop_rot_dir_button_mngr.show_prop_rot_dir_buttons()
                    if motion.prop_rot_dir == CLOCKWISE:
                        prop_rot_dir_button_mngr.cw_button.press()
                    elif motion.prop_rot_dir == COUNTER_CLOCKWISE:
                        prop_rot_dir_button_mngr.ccw_button.press()
                else:
                    prop_rot_dir_button_mngr.hide_prop_rot_dir_buttons()
        QApplication.processEvents()

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.ccw_button)
        self.top_hbox.addWidget(self.turns_box.vtg_dir_button_manager.opp_button)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.turns_box.vtg_dir_button_manager.same_button)
        self.top_hbox.addWidget(self.turns_box.prop_rot_dir_button_manager.cw_button)
        self.top_hbox.addStretch(1)
        self.separator_hbox.addWidget(self.separator)
