from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pandas as pd
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
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")

        self.setup_ui()

    def setup_ui(self) -> None:
        self.scroll_area = OptionPickerScrollArea(self.main_widget, self)
        self.filter_frame = OptionPickerFilterFrame(self)
        self.scroll_area.show_start_pos()
        self.main_layout.addWidget(self.filter_frame)
        self.main_layout.addWidget(self.scroll_area)
        self.scroll_area.show()

    def resize_option_picker_tab(self) -> None:
        self.scroll_area.resize_option_picker_scroll()

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index(["start_pos", "end_pos"], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            # Handle specific exceptions as needed
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error
