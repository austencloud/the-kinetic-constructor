from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    ICON_DIR,
)
from objects.motion.motion import Motion
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
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


class BaseIGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "IGMotionTypeAttrBox", "IGLeadStateAttrBox", "IGColorAttrBox"
        ] = attr_box
        self._initialize_ui()
        self.setup_directset_turns_buttons()

    def setup_directset_turns_buttons(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ]
    ) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()
        button_style_sheet = self._get_direct_set_button_style_sheet()
        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.clicked.connect(
                lambda checked, v=value: self._update_turns_directly(v)
            )
            self.turns_buttons_layout.addWidget(button)
        self.layout.addLayout(self.turns_buttons_layout)

    def _update_turns_directly(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        turns: str,
    ) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._set_turns(turns)

    def process_turns_adjustment_for_single_motion(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        motion: Motion,
        adjustment: float,
    ) -> None:

        new_turns = self._calculate_new_turns(motion.turns, adjustment)
        motion.set_turns(new_turns)

        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def _calculate_new_turns(self, current_turns, adjustment):
        new_turns = max(0, min(3, current_turns + adjustment))
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        return new_turns

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
        return int(self.attr_box.height() / 6)
