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
from widgets.graph_editor_tab.attr_panel.attr_panel import AttrPanel

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
        self.attr_panel = None
        self._setup_filters()

    def _setup_filters(self):
        # Initialize AttrPanel
        self.attr_panel = AttrPanel(self.tab.graph_editor)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Filters"), alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.attr_panel)

    def apply_filters(self):
        # Logic to apply filters based on attributes set in AttrPanel
        pass  # Implement the logic to apply filters

    def connect_filter_buttons(self):
        # Connect signals from AttrPanel to apply_filters
        pass  # Implement the connection logic
