from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget

from widgets.image_generator_tab.ig_pictograph import IG_Pictograph

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import ImageGeneratorTab
    from widgets.main_widget import MainWidget


class IG_Scroll_Area(QScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "ImageGeneratorTab"):
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
        self.ig_pictographs: List[IG_Pictograph] = []

    def update_displayed_pictographs(self):
        """
        Updates the displayed pictographs based on the selected letters.
        """
        # Clear existing widgets in the layout
        while self.pictograph_layout.count():
            widget = self.pictograph_layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        # Filter pictographs for selected letters
        filtered_pictographs = self.ig_tab.pictograph_df[
            self.ig_tab.pictograph_df["letter"].isin(self.ig_tab.selected_pictographs)
        ]

        # Display pictographs as views in the scroll area
        for i, (index, pictograph_data) in enumerate(filtered_pictographs.iterrows()):
            ig_pictograph = IG_Pictograph(
                self.main_widget,
                self,
            )
            # Add the option view to the grid layout
            row = i // self.COLUMN_COUNT
            col = i % self.COLUMN_COUNT
            self.pictograph_layout.addWidget(ig_pictograph.view, row, col)
            self.ig_pictographs.append(ig_pictograph)

        # Update the container size based on the content
        self.pictograph_container.setMinimumSize(self.pictograph_layout.sizeHint())
