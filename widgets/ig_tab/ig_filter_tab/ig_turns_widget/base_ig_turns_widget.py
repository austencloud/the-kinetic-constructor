from typing import TYPE_CHECKING, Union
from constants import BLUE, CLOCKWISE, DASH, ICON_DIR, NO_ROT, RED, STATIC
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QHBoxLayout
from objects.motion.motion import Motion
from ....attr_box_widgets.base_turns_widget import BaseTurnsWidget
from ....attr_panel.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from ..by_color.ig_color_attr_box import IGColorAttrBox
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox
    from ..by_lead_state.ig_lead_state_attr_box import IGLeadStateAttrBox
    from .ig_color_turns_widget import IGColorTurnsWidget
    from .ig_lead_state_turns_widget import IGLeadStateTurnsWidget
    from .ig_motion_type_turns_widget import IGMotionTypeTurnsWidget

from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt


class BaseIGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "IGMotionTypeAttrBox", "IGLeadStateAttrBox", "IGColorAttrBox"
        ] = attr_box
        self.turns_display = QLabel(
            "0", self
        )  # Initialize the QLabel with "0" as default text.
        self.turns_display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center the text.
        self._initialize_ui()
        self.setup_direct_set_turns_buttons()

    def setup_direct_set_turns_buttons(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ]
    ) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()  # Create a horizontal layout
        button_style_sheet = self._get_direct_set_button_style_sheet()

        # Create buttons and add them to the turns_buttons_layout
        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.setContentsMargins(0, 0, 0, 0)
            button.setMinimumWidth(
                button.fontMetrics().boundingRect(value).width() + 10
            )
            button.clicked.connect(lambda checked, v=value: self._direct_set_turns(v))
            self.turns_buttons_layout.addWidget(button)

        # Use a dedicated frame to hold the turns buttons
        self.turns_buttons_frame = QFrame(self)
        self.turns_buttons_frame.setLayout(self.turns_buttons_layout)

        # Add the frame to the main layout of the widget
        self.layout.addWidget(self.turns_buttons_frame)

    def create_frame(self) -> QFrame:
        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        return frame

    def _direct_set_turns(
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
        other_motion = motion.scene.motions[RED if motion.color == BLUE else BLUE]

        new_turns = self._calculate_new_turns(motion.turns, adjustment)
        if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
            motion.prop_rot_dir = NO_ROT
            for button in self.attr_box.header_widget.same_opp_buttons:
                button.setStyleSheet(self.get_button_style(pressed=False))
        simulate_same_click = False

        if new_turns > 0 and motion.motion_type in [DASH, STATIC]:
            if motion.turns == 0:
                simulate_same_click = True
                motion.prop_rot_dir = other_motion.prop_rot_dir
            if simulate_same_click:
                if (
                    not self.attr_box.header_widget.same_button.isChecked()
                    and not self.attr_box.header_widget.opp_button.isChecked()
                ):
                    self._simulate_same_button_click_in_header_widget()

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

    ### EVENT HANDLERS ###

    def update_ig_turnbox_size(self) -> None:
        """Update the size of the turns display for motion type."""
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = (
            min(self.turns_display.width(), self.turns_display.height()) * 0.25
        )
        box_font_size = int(self.attr_box.width() / 14)

        self.turns_display.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turns_display.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turns_display.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turns_display.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_display.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

        # Adjust the stylesheet to match the combo box style without the arrow
        self.turns_display.setStyleSheet(
            f"""
            QLabel {{
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def update_turns_display(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        turns: Union[int, float],
    ) -> None:
        """Update the turns display based on the latest turns value."""
        self.turns_display.setText(str(turns))

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
