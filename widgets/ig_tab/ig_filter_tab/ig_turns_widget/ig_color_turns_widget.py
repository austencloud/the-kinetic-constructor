from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
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
        self.update_ig_color_turnbox_size()
        # self.update_add_subtract_button_size()

    def adjust_turns_by_color(self, pictograph: Pictograph, adjustment: float) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        new_turns = None
        for motion in pictograph.motions.values():
            if motion.color == self.attr_box.color:
                self.process_turns_adjustment_for_single_motion(motion, adjustment)
                new_turns = motion.turns
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        self.update_turns_display(new_turns)

    def _update_turns_directly_by_color(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._set_turns_by_color(turns)

    def _set_turns_by_color(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.color == self.attr_box.color:
                    if motion.motion_type == STATIC and motion.turns == 0:
                        if (
                            not self.attr_box.header_widget.cw_button.isChecked()
                            and not self.attr_box.header_widget.ccw_button.isChecked()
                        ):
                            self._simulate_cw_button_click_in_attr_box_widget()
                        elif self.attr_box.header_widget.cw_button.isChecked():
                            motion.prop_rot_dir = CLOCKWISE
                        else:
                            motion.prop_rot_dir = COUNTER_CLOCKWISE
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
                            self.attr_box.prop_rot_dir_widget._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self.attr_box.prop_rot_dir_widget._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    def adjust_turns_incrementally_by_color(self, adjustment) -> None:
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_by_color(pictograph, adjustment)

    def _update_pictographs_turns_by_color(self, new_turns) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.color == self.attr_box.color:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self.attr_box.prop_rot_dir_widget._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self.attr_box.prop_rot_dir_widget._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    ### EVENT HANDLERS ###

    def update_ig_color_turnbox_size(self) -> None:
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

    def resize_turns_widget(self) -> None:
        self.update_ig_color_turnbox_size()
        self.update_add_subtract_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on color."""
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_by_color(pictograph, adjustment)

    def _adjust_turns_callback(self, adjustment: float) -> None:
        self.adjust_turns_incrementally_by_color(adjustment)

    def _simulate_cw_button_click_in_attr_box_widget(self) -> None:
        self.attr_box.prop_rot_dir_widget.cw_button.setChecked(True)
        self.attr_box.prop_rot_dir_widget.cw_button.click()

    def _set_turns(self, new_turns: int | float) -> None:
        self._set_turns_by_color(new_turns)
