from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, List, Union
from constants import (
    BLUE,
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
from widgets.filter_frame.attr_box.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
    BaseTurnsWidget,
)
from widgets.filter_frame.attr_box.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from widgets.filter_frame.attr_box.lead_state_attr_box import LeadStateAttrBox


class LeadStateTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "LeadStateAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: LeadStateAttrBox = attr_box


    def _update_turns_directly_by_lead_state(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._set_turns_by_lead_state(turns)

    def _set_turns_by_lead_state(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.turn_display_manager.update_turns_display(new_turns)
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.arrow.motion.lead_state == self.attr_box.lead_state:
                    motion.set_motion_turns(new_turns)
                    self.update_pictograph_dict(motion, new_turns)




    def update_ig_lead_state_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = (
            min(self.turn_display_manager.turns_display.width(), self.turn_display_manager.turns_display.height()) * 0.25
        )
        box_font_size = int(self.attr_box.width() / 14)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = (
            min(self.turn_display_manager.turns_display.width(), self.turn_display_manager.turns_display.height()) * 0.25
        )
        turns_label_font = QFont("Arial", int(self.width() / 25))
        turnbox_font = QFont("Arial", box_font_size, QFont.Weight.Bold)

        self.turn_display_manager.turns_display.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turn_display_manager.turns_display.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turn_display_manager.turns_display.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turn_display_manager.turns_display.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(turns_label_font)
        self.turn_display_manager.turns_display.setFont(turnbox_font)

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turn_display_manager.turns_display.setStyleSheet(
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

    def get_trailing_motions(self) -> List[Motion]:
        trailing_motions = []
        for pictograph in self.attr_box.get_pictographs():
            leading_motion = pictograph.get_leading_motion()
            trailing_motion = (
                pictograph.motions[RED]
                if leading_motion.color == BLUE
                else pictograph.motions[BLUE]
            )
            if trailing_motion:
                trailing_motions.append(trailing_motion)
        return trailing_motions

    def get_leading_motions(self) -> List[Motion]:
        leading_motions = []
        for pictograph in self.attr_box.get_pictographs():
            leading_motion = pictograph.get_leading_motion()
            if leading_motion:
                leading_motions.append(leading_motion)
        return leading_motions

    def _simulate_cw_button_click_in_attr_box_widget(self) -> None:
        self.attr_box.vtg_dir_widget.same_button.setChecked(True)
        self.attr_box.vtg_dir_widget.same_button.click()

    def _simulate_cw_button_click(self) -> None:
        self.attr_box.vtg_dir_widget.same_button.setChecked(True)
        self.attr_box.vtg_dir_widget.same_button.click()

    ### EVENT HANDLERS ###

    def update_ig_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = (
            min(self.turn_display_manager.turns_display.width(), self.turn_display_manager.turns_display.height()) * 0.25
        )
        box_font_size = int(self.attr_box.width() / 14)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = (
            min(self.turn_display_manager.turns_display.width(), self.turn_display_manager.turns_display.height()) * 0.25
        )
        turns_label_font = QFont("Arial", int(self.width() / 25))
        turnbox_font = QFont("Arial", box_font_size, QFont.Weight.Bold)

        self.turn_display_manager.turns_display.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turn_display_manager.turns_display.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turn_display_manager.turns_display.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turn_display_manager.turns_display.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(turns_label_font)
        self.turn_display_manager.turns_display.setFont(turnbox_font)

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turn_display_manager.turns_display.setStyleSheet(
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


    def _set_turns(self, new_turns: int | float) -> None:
        self._set_turns_by_lead_state(new_turns)
