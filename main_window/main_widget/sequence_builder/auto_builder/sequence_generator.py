from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from typing import TYPE_CHECKING

from .circular.circular_auto_builder_frame import CircularAutoBuilderFrame
from .freeform.freeform_auto_builder_frame import FreeformAutoBuilderFrame


if TYPE_CHECKING:

    from main_window.main_widget.main_widget import MainWidget


class SequenceGeneratorWidget(QTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.background_manager = None
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.layout.addWidget(self)
        self.freeform_builder_frame = FreeformAutoBuilderFrame(self)
        self.circular_builder_frame = CircularAutoBuilderFrame(self)
        self.addTab(self.freeform_builder_frame, "Freeform")
        self.addTab(self.circular_builder_frame, "Circular")
        self.tabBar().setCursor(Qt.CursorShape.PointingHandCursor)
        self.current_auto_builder = None
        self.currentChanged.connect(self.on_tab_changed)

    def load_last_used_auto_builder(self, builder_type: str):
        """Load the last used auto builder (Freeform or Circular)."""
        if builder_type == "freeform":
            self.setCurrentWidget(self.freeform_builder_frame)
        elif builder_type == "circular":
            self.setCurrentWidget(self.circular_builder_frame)

    def get_current_auto_builder_type(self) -> str:
        """Return the currently open auto builder type."""
        return self.current_auto_builder

    def on_tab_changed(self, index: int):
        """Handle tab change event to update the current auto builder type."""
        current_widget = self.currentWidget()

        if current_widget == self.freeform_builder_frame:
            self.current_auto_builder = "freeform"
        elif current_widget == self.circular_builder_frame:
            self.current_auto_builder = "circular"

        # Update settings for the current auto builder
        self.main_widget.settings_manager.builder_settings.auto_builder.update_current_auto_builder(
            self.current_auto_builder
        )

    def resize_sequence_generator(self):
        """Resize handler for the auto builder UI."""
        # Resize the tab widget and its contents
        tab_font_size = self.main_widget.width() // 50
        tab_font = self.font()
        tab_font.setPointSize(tab_font_size)
        self.setFont(tab_font)

        # Resize the builder frames
        self.freeform_builder_frame._resize_auto_builder_frame()
        self.circular_builder_frame._resize_auto_builder_frame()

