from typing import TYPE_CHECKING, Dict, List
from constants import LETTER
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area import PictographScrollArea
from Enums import Letter
from constants import IG_PICTOGRAPH, OPTION

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class IGScrollArea(PictographScrollArea):
    def __init__(self, main_widget: "MainWidget", ig_tab: "IGTab") -> None:
        super().__init__(main_widget, ig_tab)
        self.main_widget = main_widget
        self.ig_tab = ig_tab

    def update_scroll_area_content(self) -> None:
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    def update_pictographs(self) -> None:
        """
        Updates the displayed pictographs based on the selected letters.
        """
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        filtered_pictograph_dicts: Dict[Letter, List] = {
            letter: values
            for letter, values in self.letters.items()
            if letter in self.parent_tab.selected_letters
        }

        index = 0  # Initialize an index to keep track of the pictograph's position
        for pictograph_dict_list in filtered_pictograph_dicts.values():
            for pictograph_dict in pictograph_dict_list:
                ig_pictograph: IGPictograph = self._create_pictograph(
                    pictograph_dict, IG_PICTOGRAPH
                )
                row = index // self.COLUMN_COUNT  # Calculate the row number
                col = index % self.COLUMN_COUNT   # Calculate the column number
                self.layout.addWidget(ig_pictograph.view, row, col)
                self.pictographs[ig_pictograph.current_letter] = ig_pictograph
                ig_pictograph.view.resize_for_scroll_area()
                index += 1 