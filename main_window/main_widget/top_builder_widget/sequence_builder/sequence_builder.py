from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
    AutoBuilder,
)
from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
    ManualBuilder,
)

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.top_builder_widget import (
        TopBuilderWidget,
    )


class SequenceBuilder(QTabWidget):
    def __init__(self, top_builder_widget: "TopBuilderWidget") -> None:
        super().__init__(top_builder_widget)
        self.top_builder_widget = top_builder_widget
        self.main_widget = top_builder_widget.main_widget

        # Create instances of ManualBuilder and AutoBuilder
        self.manual_builder = ManualBuilder(self)
        self.auto_builder = AutoBuilder(self)

        # Add tabs for both builders
        self.addTab(self.manual_builder, "Manual Builder")
        self.addTab(self.auto_builder, "Auto Builder")

        # Set initial tab to manual builder
        self.setCurrentIndex(0)

        # resize on tab change
        self.currentChanged.connect(self.resize_sequence_builder_tab_widget)

    def resize_sequence_builder_tab_widget(self):
        self.manual_builder.resize_manual_builder()
        self.auto_builder.resize_auto_builder()
