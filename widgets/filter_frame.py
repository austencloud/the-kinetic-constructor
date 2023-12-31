from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import (
    QPushButton,
    QButtonGroup,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtGui import QFont
from Enums import Orientation
from constants import *

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
    from widgets.option_picker_tab.option_picker_filter_frame import (
        OptionPickerFilterFrame,
    )
from PyQt6.QtCore import Qt


class FilterFrame(QFrame):
    def __init__(self, tab: Union["OptionPickerTab", "IGTab"]) -> None:
        super().__init__(tab)
        self.tab = tab
        self.row1_layouts = {}  # Layouts for whole turns for each color
        self._setup_filters()

    def _setup_filters(self):
        self._create_button_groups()
        self._setup_layouts()
        self._add_widgets()

    def _create_button_groups(self: Union["IGFilterFrame", "OptionPickerFilterFrame"]):
        self.button_groups = {
            BLUE_TURNS: QButtonGroup(self),
            RED_TURNS: QButtonGroup(self),
            BLUE_START_ORI: QButtonGroup(self),
            RED_START_ORI: QButtonGroup(self),
            BLUE_END_ORI: QButtonGroup(self),
            RED_END_ORI: QButtonGroup(self),
        }
        for key in self.button_groups.keys():
            if "turns" in key:
                self.row1_layouts[key] = QHBoxLayout()
                turns = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
                for idx, turn_value in enumerate(turns):
                    self._add_turn_button(key, turn_value, self.row1_layouts[key], idx)
            else:
                ori_id_counter = 0
                for ori in ["in", "out", "clock", "counter"]:
                    button = QPushButton(ori, self)
                    font = QFont("Arial", 11)
                    font.setBold(True)
                    button.setFont(font)
                    self.button_groups[key].addButton(button, ori_id_counter)
                    button.clicked.connect(
                        lambda checked, value=ori, group=key: self.on_button_clicked(
                            group, value
                        )
                    )
                    ori_id_counter += 1

        self.button_groups[BLUE_TURNS].button(0).setChecked(True)
        self.button_groups[RED_TURNS].button(0).setChecked(True)
        self.button_groups[BLUE_START_ORI].button(0).setChecked(True)
        self.button_groups[RED_START_ORI].button(0).setChecked(True)

    def _add_turn_button(self, key, turn_value, layout: QHBoxLayout, button_id: int):
        button = QPushButton(turn_value, self)
        self.button_groups[key].addButton(button, button_id)
        button.clicked.connect(
            lambda checked, value=turn_value, group=key: self.on_button_clicked(
                group, value
            )
        )
        font = QFont("Arial", 11)
        font.setBold(True)
        button.setFont(font)
        layout.addWidget(button)

    def _setup_layouts(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)

    def _add_widgets(self):
        vbox_layout = QVBoxLayout()

        vbox_layout.addWidget(QLabel("Left Turns"), alignment=Qt.AlignmentFlag.AlignTop)
        vbox_layout.addLayout(self.row1_layouts[BLUE_TURNS])

        vbox_layout.addWidget(
            QLabel("Right Turns"), alignment=Qt.AlignmentFlag.AlignTop
        )
        vbox_layout.addLayout(self.row1_layouts[RED_TURNS])

        self._add_group_to_layout(vbox_layout, BLUE_START_ORI, "Left Start Orientation")
        self._add_group_to_layout(vbox_layout, BLUE_END_ORI, "Left End Orientation")

        self._add_group_to_layout(vbox_layout, RED_START_ORI, "Right Start Orientation")
        self._add_group_to_layout(vbox_layout, RED_END_ORI, "Right End Orientation")

        self.layout.addLayout(vbox_layout)

    def _add_group_to_layout(self, layout: QHBoxLayout, group_key, label_text):
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(QLabel(label_text))
        for button in self.button_groups[group_key].buttons():
            hbox_layout.addWidget(button)
        layout.addLayout(hbox_layout)
