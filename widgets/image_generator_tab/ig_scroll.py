from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
from Enums import Letter, Orientation
from utilities.TypeChecking.TypeChecking import Turns

from widgets.image_generator_tab.ig_pictograph import IGPictograph

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScroll(QScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab
        self.pictograph_container = QWidget()
        self.pictograph_layout = QGridLayout(self.pictograph_container)
        self.pictograph_layout.setSpacing(10)
        self.setWidgetResizable(True)
        self.setWidget(self.pictograph_container)
        self.COLUMN_COUNT = 4
        self.spacing = 10
        self.ig_pictographs: Dict[Letter, IGPictograph] = {}

    def apply_turn_filters(self, filters: Dict[str, Union[Turns, Orientation]]) -> None:
        for ig_pictograph in self.ig_pictographs.values():
            if ig_pictograph.meets_turn_criteria(filters):
                self.update_displayed_pictographs()

    def update_displayed_pictographs(self) -> None:
        """
        Updates the displayed pictographs based on the selected letters.
        """
        while self.pictograph_layout.count():
            widget = self.pictograph_layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        filtered_pictographs = self.ig_tab.pictograph_df[
            self.ig_tab.pictograph_df["letter"].isin(self.ig_tab.selected_pictographs)
        ]

        for i, (index, pictograph_data) in enumerate(filtered_pictographs.iterrows()):
            ig_pictograph: IGPictograph = self.ig_tab._create_ig_pictograph(
                pictograph_data
            )
            # Add the pictograph view to the layout
            row = i // self.COLUMN_COUNT
            col = i % self.COLUMN_COUNT
            self.pictograph_layout.addWidget(ig_pictograph.view, row, col)
            self.ig_pictographs[ig_pictograph.current_letter] = ig_pictograph
            # Update the pictograph to reflect the new items
            ig_pictograph.update_pictograph()
            # Resize the view to fit the scene
            ig_pictograph.view.resize_ig_pictograph()

        self.update_scroll_area_content()

    def resize_ig_scroll_area(self) -> None:
        for ig_pictograph in self.ig_pictographs:
            ig_pictograph.view.resize_ig_pictograph()

    def update_scroll_area_content(self):
        self.pictograph_container.adjustSize()
        self.pictograph_layout.update()
        self.updateGeometry()
