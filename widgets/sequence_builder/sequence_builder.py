from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from ..sequence_builder.sequence_builder_scroll_area import SequenceBuilderScrollArea
from ..sequence_builder.clickable_option_handler import SequenceBuilderClickableOptionHandler
from ..sequence_builder.start_position_handler import StartPositionHandler
from ..scroll_area.components.sequence_builder_display_manager import (
    SequenceBuilderDisplayManager,
)
from ..scroll_area.components.section_manager.section_manager import (
    ScrollAreaSectionManager,
)
from ..scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self._setup_components()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)

    def _setup_components(self):
        self.clickable_option_handler = SequenceBuilderClickableOptionHandler(self)
        self.display_manager = SequenceBuilderDisplayManager(self)
        self.sections_manager = ScrollAreaSectionManager(self)
        self.scroll_area = SequenceBuilderScrollArea(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self.scroll_area)
        self.start_position_handler = StartPositionHandler(self)

    def resize_sequence_builder(self) -> None:
        self.scroll_area.resize_sequence_builder_scroll_area()
