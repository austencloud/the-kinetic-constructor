from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from widgets.sequence_builder.components.sequence_builder_section_manager import SequenceBuilderSectionManager

from .components.sequence_builder_scroll_area import SequenceBuilderScrollArea
from .components.clickable_option_handler import (
    SequenceBuilderClickableOptionHandler,
)
from .components.start_position_handler import StartPositionHandler
from ..scroll_area.components.sequence_builder_display_manager import (
    SequenceBuilderDisplayManager,
)
from ..scroll_area.components.section_manager.section_manager import (
    CodexSectionManager,
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
        self.sections_manager = CodexSectionManager(self)
        self.scroll_area = SequenceBuilderScrollArea(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self.scroll_area)
        self.start_position_handler = StartPositionHandler(self)
        # self.filter_tab_manager = self.main_widget.filter_tab_manager

    def resize_sequence_builder(self) -> None:
        self.scroll_area.resize_sequence_builder_scroll_area()

    def transition_to_sequence_building(self):
        # Ensure the specialized Section Manager is used and initialized
        if not self.sections_manager_loaded:
            self.sections_manager = SequenceBuilderSectionManager(self.scroll_area)
            self.sections_manager_loaded = True

        # Update UI components for sequence building
        self.sections_manager.update_sections_for_sequence_context(self.start_position)
        self.letter_button_frame.show()
        self.scroll_area.show()