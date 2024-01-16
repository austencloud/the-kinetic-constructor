from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pandas as pd

from constants import END_POS, START_POS
from widgets.filter_frame.filter_tab.filter_tab import FilterTab
from .option_picker_scroll_area import OptionPickerScrollArea

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class OptionPickerTab(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_area = OptionPickerScrollArea(self.main_widget, self)

        self.filter_tab = FilterTab(self.scroll_area)

        self.layout.addWidget(self.filter_tab)
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.show()

    def resize_option_picker_tab(self) -> None:
        self.scroll_area.resize_option_picker_scroll()

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index([START_POS, END_POS], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def resize_tab(self) -> None:
        if self.filter_tab.motion_type_attr_panel.isVisible():
            self.filter_tab.motion_type_attr_panel.resize_ig_motion_type_attr_panel()
        elif self.filter_tab.color_attr_panel.isVisible():
            self.filter_tab.color_attr_panel.resize_ig_color_attr_panel()
        elif self.filter_tab.lead_state_attr_panel.isVisible():
            self.filter_tab.lead_state_attr_panel.resize_ig_lead_state_attr_panel()
