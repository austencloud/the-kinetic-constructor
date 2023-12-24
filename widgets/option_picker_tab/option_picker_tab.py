from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from .option_picker_scroll_area import OptionPickerScrollArea

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from widgets.option_picker_tab.option_picker_filter_frame import OptionPickerFilterFrame


class OptionPickerTab(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.scroll_area = OptionPickerScrollArea(self.main_widget, self)
        self.filter_frame = OptionPickerFilterFrame(self)
        self.scroll_area._show_start_position()
        self.main_layout.addWidget(self.filter_frame)
        self.main_layout.addWidget(self.scroll_area)
        self.scroll_area.show()

    def resize_option_picker_tab(self) -> None:
        self.scroll_area.resize_option_picker_scroll()
