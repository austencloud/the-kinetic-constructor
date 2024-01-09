from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR, NO_ROT
from objects.motion.motion import Motion
from .base_ig_turns_widget import BaseIGTurnsWidget
if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGMotionTypeAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.setup_directset_turns_buttons()
        self.turnbox.currentIndexChanged.connect(self.update_turns_directly)

    def update_turns_incrementally(self, adjustment: float) -> None:
        self.turnbox.currentIndexChanged.disconnect(self.update_turns_directly)
        self.process_turns_for_all_motions(adjustment)
        self.turnbox.currentIndexChanged.connect(self.update_turns_directly)

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

    def _simulate_cw_button_click(self):
        header_widget = self.attr_box.header_widget
        header_widget.cw_button.setChecked(True)
        header_widget.cw_button.click()

    def _get_current_prop_rot_dir_for_ig_motion_type_turns_widget(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.header_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.header_widget.ccw_button.isChecked()
            else NO_ROT
        )

    def update_turns_directly(self, turns: Union[int, float]) -> None:
        if not turns:
            return
        self._update_pictographs_turns_by_color(turns)

    def _update_pictographs_turns_by_color(self, new_turns):
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    motion.set_turns(new_turns)
                    pictograph_dict = {
                        f"{motion.color}_turns": new_turns,
                    }
                    motion.scene.update_pictograph(pictograph_dict)

    ### EVENT HANDLERS ###

    def update_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 10)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

        self.turnbox.setMinimumHeight(int(self.attr_box.width() / 4))
        self.turnbox.setMaximumHeight(int(self.attr_box.width() / 4))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

        # self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        # self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(QFont("Arial", int(self.width() / 22)))

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

    def update_button_size(self) -> None:
        for button in self.turns_buttons:
            button_size = self.calculate_button_size()
            button.update_attr_box_turns_button_size(button_size)

    def calculate_button_size(self) -> int:
        return int(self.attr_box.width() / 5)

    def resize_turns_widget(self) -> None:
        self.update_turnbox_size()
        self.update_button_size()

    def setup_directset_turns_buttons(self) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()
        button_style_sheet = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #c0c0c0;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #e5e5e5;
            border-color: #a0a0a0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """
        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.clicked.connect(
                lambda checked, v=value: self.update_turns_directly(v)
            )
            self.turns_buttons_layout.addWidget(button)
        self.layout.addLayout(self.turns_buttons_layout)
