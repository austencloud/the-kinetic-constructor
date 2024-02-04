from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pandas as pd

from constants import END_POS, START_POS
from widgets.sequence_builder.sequence_builder_scroll_area import SequenceBuilderScrollArea

if TYPE_CHECKING:
    from widgets.main_tab_widget.main_tab_widget import MainTabWidget
    from widgets.main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self.setup_ui()

    def setup_ui(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_area = SequenceBuilderScrollArea(self)

        self.layout.addWidget(self.scroll_area)
        self.scroll_area.show()

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index([START_POS, END_POS], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def resize_sequence_builder(self) -> None:
        self.scroll_area.resize_sequence_builder_scroll_area()