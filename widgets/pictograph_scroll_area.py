from typing import TYPE_CHECKING, Dict, List, Literal, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
from constants import IG_PICTOGRAPH, OPTION
from utilities.TypeChecking.TypeChecking import Orientations, Turns, Letters

from PyQt6.QtCore import Qt
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.ig_tab.ig_scroll.ig_scroll import IGScrollArea
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    COLUMN_COUNT = 6
    SPACING = 10

    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters: Dict[Letters, List[Dict[str, str]]] = self.main_widget.letters
        self.pictographs: Dict[Letters, Union["IGPictograph", "Option"]] = {}

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QGridLayout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def apply_filters(
        self: Union["OptionPickerScrollArea", "IGScrollArea"],
        filters: Dict[str, Union[Turns, Orientations]],
    ) -> None:
        for ig_pictograph in self.pictographs.values():
            if ig_pictograph._meets_criteria(filters):
                self.update_pictographs()



    ### PICTOGRAPH CREATION ###

    def _create_pictograph(
        self,
        graph_type: Literal["option", "ig_pictograph"],
    ) -> Option | IGPictograph:
        if graph_type == OPTION:
            pictograph = Option(self.main_widget, self)
        elif graph_type == IG_PICTOGRAPH:  
            pictograph = IGPictograph(self.main_widget, self)

        return pictograph
