from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
)

from Enums import Orientation
from constants.string_constants import CLOCK, COUNTER, IN, OUT

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.option_picker_tab.option_picker_filter_frame import (
        OptionPickerFilterFrame,
    )


class FilterFrame(QFrame):
    def __init__(self, tab: Union["OptionPickerTab", "IGTab"]) -> None:
        super().__init__(tab)
        self.tab = tab
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self._setup_filters()

    def _setup_filters(self) -> None:
        # Separate checkboxes for left (blue) and right (red) turns
        self.blue_turn_checkboxes: Dict[str, QCheckBox] = {}
        self.red_turn_checkboxes: Dict[str, QCheckBox] = {}
        turns_hbox: QHBoxLayout = QHBoxLayout()
        left_turn_vbox = QVBoxLayout()
        right_turn_vbox = QVBoxLayout()

        turns_hbox.addLayout(left_turn_vbox)
        turns_hbox.addLayout(right_turn_vbox)

        left_turn_vbox.addWidget(QLabel("Blue Turns:"))
        for turn_value in ["fl", 0, 0.5, 1, 1.5, 2, 2.5, 3]:
            checkbox = QCheckBox(str(turn_value), self)
            left_turn_vbox.addWidget(checkbox)
            self.blue_turn_checkboxes[str(turn_value)] = checkbox

        right_turn_vbox.addWidget(QLabel("Red Turns:"))
        for turn_value in ["fl", 0, 0.5, 1, 1.5, 2, 2.5, 3]:
            checkbox = QCheckBox(str(turn_value), self)
            right_turn_vbox.addWidget(checkbox)
            self.red_turn_checkboxes[str(turn_value)] = checkbox

        self.layout.addLayout(turns_hbox)

        self.layout.addWidget(QLabel("Left End Orientation:"))
        self.left_end_orientation_combobox = QComboBox(self)
        self.left_end_orientation_combobox.addItems([IN, OUT, CLOCK, COUNTER])
        self.layout.addWidget(self.left_end_orientation_combobox)

        self.layout.addWidget(QLabel("Right End Orientation:"))
        self.right_end_orientation_combobox = QComboBox(self)
        self.right_end_orientation_combobox.addItems([IN, OUT, CLOCK, COUNTER])
        self.layout.addWidget(self.right_end_orientation_combobox)

        self.blue_turn_checkboxes["0"].setChecked(True)
        self.red_turn_checkboxes["0"].setChecked(True)

    def connect_filter_boxes(self: Union["OptionPickerFilterFrame", "IGFilterFrame"]):
        for checkbox in self.blue_turn_checkboxes.values():
            checkbox.stateChanged.connect(self.apply_filters)
        for checkbox in self.red_turn_checkboxes.values():
            checkbox.stateChanged.connect(self.apply_filters)
        self.apply_filters()
        self.left_end_orientation_combobox.currentTextChanged.connect(
            self.apply_filters
        )
        self.right_end_orientation_combobox.currentTextChanged.connect(
            self.apply_filters
        )
