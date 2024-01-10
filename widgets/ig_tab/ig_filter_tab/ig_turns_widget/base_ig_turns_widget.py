from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, List, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    RED,
    STATIC,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import Colors
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)
from widgets.attr_panel.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_box import IGColorAttrBox
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_box import (
        IGMotionTypeAttrBox,
    )
    from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import (
        IGLeadStateAttrBox,
    )
    from .ig_color_turns_widget import IGColorTurnsWidget
    from .ig_lead_state_turns_widget import IGLeadStateTurnsWidget
    from .ig_motion_type_turns_widget import IGMotionTypeTurnsWidget

from PyQt6.QtCore import pyqtBoundSignal


class BaseIGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "IGMotionTypeAttrBox", "IGLeadStateAttrBox", "IGColorAttrBox"
        ] = attr_box
        self._initialize_ui()

    def process_turns_adjustment_for_single_motion(
        self: "IGMotionTypeTurnsWidget", motion: Motion, adjustment: float
    ) -> None:
        from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_box import (
            IGMotionTypeAttrBox,
        )

        initial_turns = motion.turns
        new_turns = self._calculate_new_turns(motion.turns, adjustment)

        motion.set_turns(new_turns)

        if motion.is_dash_or_static() and self._turns_added(initial_turns, new_turns):
            if isinstance(self.attr_box, IGMotionTypeAttrBox):
                self._simulate_cw_button_click_in_header_widget()
            else:
                self._simulate_cw_button_click_in_attr_box_widget()
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def _calculate_new_turns(self, current_turns, adjustment):
        return max(0, min(3, current_turns + adjustment))

    def update_turns_display(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        turns: Union[int, float],
    ) -> None:
        turns_str = str(turns)
        self.turnbox.setCurrentText(turns_str)

    ### EVENT HANDLERS ###

    def update_ig_turnbox_size(self) -> None:
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
        for turns_button in self.add_subtract_buttons:
            button_size = self.calculate_turns_button_size()
            turns_button.update_attr_box_turns_button_size(button_size)

    def calculate_turns_button_size(self) -> int:
        return int(self.attr_box.width() / 10)

    def resize_turns_widget(self) -> None:
        self.update_ig_turnbox_size()
        self.update_ig_lead_state_turns_button_size()


    def update_add_subtract_button_size(self) -> None:
        for button in self.add_subtract_buttons:
            button_size = self.calculate_button_size()
            button.update_attr_box_turns_button_size(button_size)

    def calculate_button_size(self) -> int:
        return int(self.attr_box.height() / 3.5)
