from typing import TYPE_CHECKING, Dict, List, Literal, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
from Enums import Letter, Orientation, PictographAttributesDict
from constants import END_POS, IG_PICTOGRAPH, LETTER, OPTION, START_POS
from utilities.TypeChecking.TypeChecking import Turns
from PyQt6.QtCore import Qt
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.image_generator_tab.ig_scroll import IGScrollArea
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
        self.pictographs: Dict[Letter, Union["IGPictograph", "Option"]] = {}

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
        filters: Dict[str, Union[Turns, Orientation]],
    ) -> None:
        for ig_pictograph in self.pictographs.values():
            if ig_pictograph._meets_criteria(filters):
                self.update_pictographs()

    def update_scroll_area_content(self):
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    ### PICTOGRAPH CREATION ###

    def _create_pictograph(
        self,
        pictograph_dict: PictographAttributesDict,
        graph_type: Literal["option", "ig_pictograph"],
    ) -> Option | IGPictograph:
        if graph_type == OPTION:
            pictograph = Option(self.main_widget, self)
        else:  # graph_type == IG_PICTOGRAPH
            pictograph = IGPictograph(self.main_widget, self)
            
        pictograph.update_pictograph(pictograph_dict)
        return pictograph
