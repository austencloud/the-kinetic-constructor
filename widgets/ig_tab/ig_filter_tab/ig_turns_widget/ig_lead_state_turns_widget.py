from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, List, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    LEADING,
    NO_ROT,
    RED,
    STATIC,
    TRAILING,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import Colors
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)
from widgets.ig_tab.ig_filter_tab.ig_turns_widget.base_ig_turns_widget import (
    BaseIGTurnsWidget,
)


if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import (
        IGLeadStateAttrBox,
    )
from PyQt6.QtCore import pyqtBoundSignal


class IGLeadStateTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGLeadStateAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box

    def update_turns_directly(self, turns: float) -> None:
        """Directly set the turns value for the motion type."""
        if turns in ["0", "1", "2", "3"]:
            self.turnbox.setCurrentText(turns)
        elif turns in ["0.5", "1.5", "2.5"]:
            self.turnbox.setCurrentText(turns)
        self.update_turns_directly()  # This method will now be triggered with the new turns value

    def set_layout_margins_and_alignment(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def connect_signals(self) -> None:
        self.turnbox.currentIndexChanged.connect(self.update_turns_directly)

    def update_turns_incrementally(self, adjustment: float) -> None:
        self.disconnect_signal(self.turnbox.currentIndexChanged)
        self.process_turns_for_all_motions(adjustment)
        self.connect_signal(self.turnbox.currentIndexChanged)

    def process_turns_for_all_motions(self, adjustment: float) -> None:
        if self.attr_box.lead_state == TRAILING:
            for motion in self.get_trailing_motions():
                self.process_update_turns(motion, adjustment)

        elif self.attr_box.lead_state == LEADING:
            for motion in self.get_leading_motions():
                self.process_update_turns(motion, adjustment)

    def determine_leading_color(
        self, red_start, red_end, blue_start, blue_end
    ) -> Colors:
        if red_start == blue_end:
            return RED
        elif blue_start == red_end:
            return BLUE
        return None

    def get_trailing_motions(self):
        trailing_motions = []
        for pictograph in self.attr_box.get_pictographs():
            red_start = pictograph.motions[RED].start_loc
            red_end = pictograph.motions[RED].end_loc
            blue_start = pictograph.motions[BLUE].start_loc
            blue_end = pictograph.motions[BLUE].end_loc
            leading_color = self.determine_leading_color(
                red_start, red_end, blue_start, blue_end
            )
            if leading_color == RED:
                trailing_color = BLUE
            elif leading_color == BLUE:
                trailing_color = RED
            if trailing_color:
                trailing_motions.append(pictograph.motions[trailing_color])
        return trailing_motions

    def get_leading_motions(self) -> List[Motion]:
        leading_motions = []
        for pictograph in self.attr_box.get_pictographs():
            red_start = pictograph.motions[RED].start_loc
            red_end = pictograph.motions[RED].end_loc
            blue_start = pictograph.motions[BLUE].start_loc
            blue_end = pictograph.motions[BLUE].end_loc
            leading_color = self.determine_leading_color(
                red_start, red_end, blue_start, blue_end
            )
            if leading_color:
                leading_motions.append(pictograph.motions[leading_color])
        return leading_motions

    def process_update_turns(self, motion: Motion, adjustment: float) -> None:
        initial_turns = motion.turns
        new_turns = self._calculate_new_turns(motion.turns, adjustment)
        self.update_turns_display(new_turns)

        motion.set_turns(new_turns)

        if motion.is_dash_or_static() and self._turns_added(initial_turns, new_turns):
            self._simulate_cw_button_click()
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def _simulate_cw_button_click(self) -> None:
        self.attr_box.prop_rot_dir_widget.cw_button.setChecked(True)
        self.attr_box.prop_rot_dir_widget.cw_button.click()

    def update_turns_directly(self) -> None:
        selected_turns_str = self.turnbox.currentText()
        if not selected_turns_str:
            return

        new_turns = float(selected_turns_str)
        self._update_pictographs_turns_by_color(new_turns)

    def _update_pictographs_turns_by_color(self, new_turns):
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.arrow.lead_state == self.attr_box.lead_state:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self._get_current_prop_rot_dir_for_ig_motion_type_turns_widget()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self._get_current_prop_rot_dir_for_ig_motion_type_turns_widget(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    def _simulate_cw_button_click(self) -> None:
        self.attr_box.prop_rot_dir_widget.cw_button.setChecked(True)
        self.attr_box.prop_rot_dir_widget.cw_button.click()

    ### EVENT HANDLERS ###

    def update_ig_lead_state_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 14)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        turns_label_font = QFont("Arial", int(self.width() / 25))
        turnbox_font = QFont("Arial", box_font_size, QFont.Weight.Bold)

        self.turnbox.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turnbox.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(turns_label_font)
        self.turnbox.setFont(turnbox_font)

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turnbox.setStyleSheet(
            f"""
            QComboBox {{
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 0px; /* make room for the arrow on the right */
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_arrow_width}px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* visually separate the arrow part */
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}
            QComboBox::down-arrow {{
                image: url("{ICON_DIR}/combobox_arrow.png");
                width: {int(dropdown_arrow_width * 0.6)}px;
                height: {int(dropdown_arrow_width * 0.6)}px;
            }}
        """
        )

    def update_ig_lead_state_turns_button_size(self) -> None:
        for turns_button in self.turns_buttons:
            button_size = self.calculate_turns_button_size()
            turns_button.update_attr_box_turns_button_size(button_size)

    def resize_turns_widget(self) -> None:
        self.update_ig_lead_state_turnbox_size()
        self.update_ig_lead_state_turns_button_size()

    def process_turns_for_all_motions(self, adjustment: float) -> None:
        if self.attr_box.lead_state == TRAILING:
            for motion in self.get_trailing_motions():
                self.process_update_turns(motion, adjustment)

        elif self.attr_box.lead_state == LEADING:
            for motion in self.get_leading_motions():
                self.process_update_turns(motion, adjustment)

    def get_trailing_motions(self):
        trailing_motions = []
        for pictograph in self.attr_box.get_pictographs():
            red_start = pictograph.motions[RED].start_loc
            red_end = pictograph.motions[RED].end_loc
            blue_start = pictograph.motions[BLUE].start_loc
            blue_end = pictograph.motions[BLUE].end_loc
            leading_color = self.determine_leading_color(
                red_start, red_end, blue_start, blue_end
            )
            if leading_color == RED:
                trailing_color = BLUE
            elif leading_color == BLUE:
                trailing_color = RED
            if trailing_color:
                trailing_motions.append(pictograph.motions[trailing_color])
        return trailing_motions

    def get_leading_motions(self) -> List[Motion]:
        leading_motions = []
        for pictograph in self.attr_box.get_pictographs():
            red_start = pictograph.motions[RED].start_loc
            red_end = pictograph.motions[RED].end_loc
            blue_start = pictograph.motions[BLUE].start_loc
            blue_end = pictograph.motions[BLUE].end_loc
            leading_color = self.determine_leading_color(
                red_start, red_end, blue_start, blue_end
            )
            if leading_color:
                leading_motions.append(pictograph.motions[leading_color])
        return leading_motions
