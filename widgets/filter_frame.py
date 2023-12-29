from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
)
from PyQt6.QtGui import QFont
from Enums import Orientation, Turns
from constants import *
if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.option_picker_tab.option_picker_filter_frame import (
        OptionPickerFilterFrame,
    )
from Enums import Orientation


class FilterFrame(QFrame):
    def __init__(self, tab: Union["OptionPickerTab", "IGTab"]) -> None:
        super().__init__(tab)
        self.tab = tab
        self._setup_filters()

    def _setup_filters(self) -> None:
        self._create_comboboxes()
        self._setup_layouts()
        self._add_widgets()
        self._add_combobox_items()
        self._set_stylesheets()
        self._set_initial_filters()

    def _create_comboboxes(self) -> None:
        self.comboboxes = {
            BLUE_TURNS: QComboBox(self),
            BLUE_START_OR: QComboBox(self),
            BLUE_END_OR: QComboBox(self),
            RED_TURNS: QComboBox(self),
            RED_START_OR: QComboBox(self),
            RED_END_OR: QComboBox(self),
        }

    def _setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)

    def _add_combobox_items(self) -> None:
        orientations = [o.value for o in list(Orientation)]
        turns = [t.value for t in list(Turns)]

        for key, combobox in self.comboboxes.items():
            if "turns" in key:
                combobox.addItems(turns)
            elif "or" in key:
                combobox.addItems(orientations)

    def _set_stylesheets(self) -> None:
        border_radius = min(self.width(), self.height()) * 0.25
        border_width = 2
        dropdown_arrow_width = int(self.width() * 0.25)
        box_font_size = int(self.width() / 7)
        font = QFont("Arial", box_font_size, QFont.Weight.Bold)

        stylesheet_template = """
            QComboBox {{
                padding-left: 2px;
                padding-right: 0px;
                border: {border_width}px solid black;
                border-radius: {border_radius}px;
                max-width: 100px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_arrow_width}px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}
            QComboBox::down-arrow {{
                image: url("{ICON_DIR}/combobox_arrow.png");
                width: {arrow_size}px;
                height: {arrow_size}px;
            }}
        """

        stylesheet = stylesheet_template.format(
            border_width=border_width,
            border_radius=border_radius,
            dropdown_arrow_width=dropdown_arrow_width,
            arrow_size=int(dropdown_arrow_width * 0.6),
            ICON_DIR=ICON_DIR,
        )

        for combobox in self.comboboxes.values():
            combobox.setFont(font)
            combobox.setStyleSheet(stylesheet)

    def _add_widgets(self) -> None:
        # Create vertical layouts for left and right sections
        left_vbox_layout = QVBoxLayout()
        right_vbox_layout = QVBoxLayout()

        # Add widgets to the left vertical layout
        left_vbox_layout.addWidget(QLabel("Left Turns:"))
        left_vbox_layout.addWidget(self.comboboxes[BLUE_TURNS])
        left_vbox_layout.addWidget(QLabel("Left Start Orientation:"))
        left_vbox_layout.addWidget(self.comboboxes[BLUE_START_OR])
        left_vbox_layout.addWidget(QLabel("Left End Orientation:"))
        left_vbox_layout.addWidget(self.comboboxes[BLUE_END_OR])

        # Add widgets to the right vertical layout
        right_vbox_layout.addWidget(QLabel("Right Turns:"))
        right_vbox_layout.addWidget(self.comboboxes[RED_TURNS])
        right_vbox_layout.addWidget(QLabel("Right Start Orientation:"))
        right_vbox_layout.addWidget(self.comboboxes[RED_START_OR])
        right_vbox_layout.addWidget(QLabel("Right End Orientation:"))
        right_vbox_layout.addWidget(self.comboboxes[RED_END_OR])

        # Add the left and right vertical layouts to the main horizontal layout
        self.layout.addLayout(left_vbox_layout)
        self.layout.addLayout(right_vbox_layout)

    def _set_initial_filters(self) -> None:
        self.comboboxes[BLUE_TURNS].setCurrentText("0")
        self.comboboxes[BLUE_START_OR].setCurrentText(IN)
        self.comboboxes[BLUE_END_OR].setCurrentIndex(-1)
        self.comboboxes[RED_TURNS].setCurrentText("0")
        self.comboboxes[RED_START_OR].setCurrentText(IN)
        self.comboboxes[RED_END_OR].setCurrentIndex(-1)


    def connect_filter_boxes(
        self: Union["OptionPickerFilterFrame", "IGFilterFrame"]
    ) -> None:
        self.comboboxes[BLUE_TURNS].currentTextChanged.connect(self.apply_filters)
        self.comboboxes[RED_TURNS].currentTextChanged.connect(self.apply_filters)
        self.comboboxes[BLUE_END_OR].currentTextChanged.connect(self.apply_filters)
        self.comboboxes[RED_END_OR].currentTextChanged.connect(self.apply_filters)
