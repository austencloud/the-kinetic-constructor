from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
import pandas as pd
from Enums import Letter, Orientation
from constants import LETTER
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import Turns
from PyQt6.QtCore import Qt
from widgets.image_generator_tab.ig_pictograph import IGPictograph

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    COLUMN_COUNT = 4
    SPACING = 10

    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters: Dict[Letter, List[Dict[str, str]]] = self.main_widget.letters
        self.pictographs: Dict[Letter, Pictograph] = {}

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QGridLayout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def apply_filters(self, filters: Dict[str, Union[Turns, Orientation]]) -> None:
        for ig_pictograph in self.pictographs.values():
            if ig_pictograph.meets_turn_criteria(filters):
                self.update_displayed_pictographs()

    def update_displayed_pictographs(self) -> None:
        """
        Updates the displayed pictographs based on the selected letters.
        """
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        filtered_pictographs = self.parent_tab.pictograph_df[
            self.parent_tab.pictograph_df["letter"].isin(
                self.parent_tab.selected_pictographs
            )
        ]

        for i, (_, pictograph_data) in enumerate(filtered_pictographs.iterrows()):
            ig_pictograph: IGPictograph = self._create_pictograph(pictograph_data)
            row = i // self.COLUMN_COUNT
            col = i % self.COLUMN_COUNT
            self.layout.addWidget(ig_pictograph.view, row, col)
            self.ig_pictographs[ig_pictograph.current_letter] = ig_pictograph
            ig_pictograph.update_pictograph()
            ig_pictograph.view.resize_ig_pictograph()

        self.update_scroll_area_content()

    def update_scroll_area_content(self):
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    ### OPTION CREATION ###

    def _create_pictograph(self, pd_row_data: pd.Series):
        ig_pictograph = IGPictograph(self.main_widget, self)
        ig_pictograph.current_letter = pd_row_data[LETTER]
        filters = self.parent_tab.filter_frame.filters
        ig_pictograph._setup_motions(pd_row_data, filters)
        ig_pictograph.update_pictograph()
        return ig_pictograph
