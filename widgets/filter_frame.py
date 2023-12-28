from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
)

from constants import CLOCK, COUNTER, IN, OUT

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
        self._setup_filters()

    def _setup_filters(self) -> None:
        self.create_comboboxes()
        self._setup_layouts()
        self._add_widgets()
        self._add_combobox_items()
        self.set_initial_filters()

    def create_comboboxes(self):
        self.left_turns_combobox = QComboBox(self)
        self.right_turns_combobox = QComboBox(self)
        self.left_start_or_combobox = QComboBox(self)
        self.right_start_or_combobox = QComboBox(self)
        self.left_end_or_combobox = QComboBox(self)
        self.right_end_or_combobox = QComboBox(self)

    def _setup_layouts(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)

    def _add_combobox_items(self):
        self.left_turns_combobox.addItems(["0", "0.5", "1", "1.5", "2", "2.5", "3"])
        self.right_turns_combobox.addItems(["0", "0.5", "1", "1.5", "2", "2.5", "3"])
        self.left_start_or_combobox.addItems([IN, OUT, CLOCK, COUNTER])
        self.right_start_or_combobox.addItems([IN, OUT, CLOCK, COUNTER])
        self.left_end_or_combobox.addItems([IN, OUT, CLOCK, COUNTER])
        self.right_end_or_combobox.addItems([IN, OUT, CLOCK, COUNTER])

    def _add_widgets(self):
        # Create vertical layouts for left and right sections
        left_vbox_layout = QVBoxLayout()
        right_vbox_layout = QVBoxLayout()

        # Add widgets to the left vertical layout
        left_vbox_layout.addWidget(QLabel("Left Turns:"))
        left_vbox_layout.addWidget(self.left_turns_combobox)
        left_vbox_layout.addWidget(QLabel("Left Start Orientation:"))
        left_vbox_layout.addWidget(self.left_start_or_combobox)
        left_vbox_layout.addWidget(QLabel("Left End Orientation:"))
        left_vbox_layout.addWidget(self.left_end_or_combobox)

        # Add widgets to the right vertical layout
        right_vbox_layout.addWidget(QLabel("Right Turns:"))
        right_vbox_layout.addWidget(self.right_turns_combobox)
        right_vbox_layout.addWidget(QLabel("Right Start Orientation:"))
        right_vbox_layout.addWidget(self.right_start_or_combobox)
        right_vbox_layout.addWidget(QLabel("Right End Orientation:"))
        right_vbox_layout.addWidget(self.right_end_or_combobox)

        # Add the left and right vertical layouts to the main horizontal layout
        self.layout.addLayout(left_vbox_layout)
        self.layout.addLayout(right_vbox_layout)

    def set_initial_filters(self):
        self.left_turns_combobox.setCurrentIndex(0)
        self.right_turns_combobox.setCurrentIndex(0)
        self.left_end_or_combobox.setCurrentIndex(-1)
        self.right_end_or_combobox.setCurrentIndex(-1)

    def connect_filter_boxes(self: Union["OptionPickerFilterFrame", "IGFilterFrame"]):
        self.left_turns_combobox.currentTextChanged.connect(self.apply_filters)
        self.right_turns_combobox.currentTextChanged.connect(self.apply_filters)
        self.left_end_or_combobox.currentTextChanged.connect(self.apply_filters)
        self.right_end_or_combobox.currentTextChanged.connect(self.apply_filters)
