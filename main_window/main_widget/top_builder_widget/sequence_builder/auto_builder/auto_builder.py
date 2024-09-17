from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .circular.circular_auto_builder_frame import CircularAutoBuilderFrame
from .freeform.freeform_auto_builder_frame import FreeformAutoBuilderFrame


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.sequence_builder import (
        SequenceBuilder,
    )
    from main_window.main_widget.main_widget import MainWidget


class AutoBuilder(QFrame):
    def __init__(self, sequence_builder_tab_widget: "SequenceBuilder") -> None:
        super().__init__(sequence_builder_tab_widget)
        self.sequence_builder = sequence_builder_tab_widget
        self.main_widget: "MainWidget" = sequence_builder_tab_widget.main_widget

        # Frame layout setup
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)

        # Create QTabWidget to hold the auto builder frames
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Create instances of the auto builder frames
        self.freeform_builder_frame = FreeformAutoBuilderFrame(self)
        self.circular_builder_frame = CircularAutoBuilderFrame(self)

        # Add frames as tabs to the tab widget
        self.tab_widget.addTab(self.freeform_builder_frame, "Freeform Builder")
        self.tab_widget.addTab(self.circular_builder_frame, "Circular Builder")

        # give the tab bar a pointing hand cursor
        self.tab_widget.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)

        # Set the current auto builder type
        self.current_auto_builder = None

        # Connect tab change event
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def load_last_used_auto_builder(self, builder_type: str):
        """Load the last used auto builder (Freeform or Circular)."""
        if builder_type == "freeform":
            self.tab_widget.setCurrentWidget(self.freeform_builder_frame)
        elif builder_type == "circular":
            self.tab_widget.setCurrentWidget(self.circular_builder_frame)

    def get_current_auto_builder_type(self) -> str:
        """Return the currently open auto builder type."""
        return self.current_auto_builder

    def on_tab_changed(self, index: int):
        """Handle tab change event to update the current auto builder type."""
        current_widget = self.tab_widget.currentWidget()

        if current_widget == self.freeform_builder_frame:
            self.current_auto_builder = "freeform"
        elif current_widget == self.circular_builder_frame:
            self.current_auto_builder = "circular"

        # Update settings for the current auto builder
        self.main_widget.settings_manager.builder_settings.auto_builder.update_current_auto_builder(
            self.current_auto_builder
        )

    def resize_auto_builder(self):
        """Resize handler for the auto builder UI."""
        # Resize the tab widget and its contents
        tab_font_size = self.width() // 50
        tab_font = self.tab_widget.font()
        tab_font.setPointSize(tab_font_size)
        self.tab_widget.setFont(tab_font)

        # Resize the builder frames
        self.freeform_builder_frame._resize_auto_builder_frame()
        self.circular_builder_frame._resize_auto_builder_frame()
