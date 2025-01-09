from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from .option_factory import OptionFactory
from .option_picker_layout_manager import OptionPickerLayoutManager
from .option_picker_updater import OptionPickerUpdater
from .option_picker_click_handler import OptionPickerClickHandler
from .scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from .reversal_filter.option_picker_reversal_filter import OptionPickerReversalFilter
from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OptionPicker(QWidget):
    """Contains the 'Choose Your Next Pictograph' label, filter combo box, and the OptionPickerScrollArea."""

    COLUMN_COUNT = 8
    option_selected = pyqtSignal(str)
    layout: QVBoxLayout
    option_pool: list["BasePictograph"]

    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.main_widget = construct_tab.main_widget
        self.json_manager = self.main_widget.json_manager
        self.fade_manager = self.main_widget.fade_manager

        # Components
        self.choose_next_label = ChooseYourNextPictographLabel(self)
        self.reversal_filter = OptionPickerReversalFilter(self)
        self.scroll_area = OptionPickerScrollArea(self)

        # Managers
        self.option_getter = OptionGetter(self)
        self.click_handler = OptionPickerClickHandler(self)
        self.updater = OptionPickerUpdater(self)
        self.option_factory = OptionFactory(self)
        self.layout_manager = OptionPickerLayoutManager(self)
