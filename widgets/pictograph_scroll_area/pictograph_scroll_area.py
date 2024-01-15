from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import (
    Letters,
)
from ..ig_tab.ig_scroll.ig_pictograph import IGPictograph
from ..option_picker_tab.option import Option
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterFrameManager
from .scroll_area_pictograph_factory import ScrollAreaPictographFactory

if TYPE_CHECKING:
    from ..option_picker_tab.option_picker_tab import OptionPickerTab
    from ..ig_tab.ig_tab import IGTab
    from ..main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters: Dict[Letters, List[Dict[str, str]]] = self.main_widget.letters
        self.pictographs: Dict[Letters, Union["IGPictograph", "Option"]] = {}

        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterFrameManager(self)
        
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QGridLayout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.order_and_display_pictographs()
        self.display_manager.cleanup_unused_pictographs()
        self.filter_frame_manager.update_filter_frame_if_needed()
