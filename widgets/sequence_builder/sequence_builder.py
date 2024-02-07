from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
import pandas as pd
from constants import END_POS, START_POS

from widgets.sequence_builder.sequence_builder_scroll_area import (
    SequenceBuilderScrollArea,
)
from widgets.sequence_builder.clickable_option_handler import ClickableOptionHandler
from widgets.sequence_builder.start_position_handler import StartPositionHandler
from widgets.scroll_area.components.sequence_builder_display_manager import (
    SequenceBuilderDisplayManager,
)
from widgets.scroll_area.components.section_manager.section_manager import (
    ScrollAreaSectionManager,
)
from widgets.scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self.clickable_option_handler = ClickableOptionHandler(self)
        self.start_position_handler = StartPositionHandler(self)
        self.display_manager = SequenceBuilderDisplayManager(self)
        self.sections_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)
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
            return pd.DataFrame()

    def resize_sequence_builder(self) -> None:
        self.scroll_area.resize_sequence_builder_scroll_area()
