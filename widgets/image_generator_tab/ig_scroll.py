from typing import TYPE_CHECKING
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area import PictographScrollArea

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScroll(PictographScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(main_widget, ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab

    def update_displayed_pictographs(self) -> None:
        """
        Updates the displayed pictographs based on the selected letters.
        """
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        filtered_pictographs = self.ig_tab.pictograph_df[
            self.ig_tab.pictograph_df["letter"].isin(self.ig_tab.selected_pictographs)
        ]

        for i, (_, pictograph_data) in enumerate(filtered_pictographs.iterrows()):
            ig_pictograph: IGPictograph = self._create_pictograph(pictograph_data)
            row = i // self.COLUMN_COUNT
            col = i % self.COLUMN_COUNT
            self.layout.addWidget(ig_pictograph.view, row, col)
            self.pictographs[ig_pictograph.current_letter] = ig_pictograph
            ig_pictograph.update_pictograph()
            ig_pictograph.view.resize_ig_pictograph()

        self.update_scroll_area_content()

    def update_scroll_area_content(self):
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()
