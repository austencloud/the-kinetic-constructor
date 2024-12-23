# build_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from main_window.main_widget.build_tab.manual_builder import ManualBuilder
from main_window.main_widget.build_tab.sequence_generator.sequence_generator_widget import SequenceGeneratorWidget
from main_window.main_widget.build_tab.sequence_widget.sequence_widget import SequenceWidget


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BuildTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Initialize SequenceWidget (shared between Build and Generate)
        self.sequence_widget = SequenceWidget(self)

        # Initialize content stack for Build and Generate
        self.content_stack = QStackedWidget(self)
        self.manual_builder = ManualBuilder(self)  # Build functionality
        self.sequence_generator = SequenceGeneratorWidget(self)  # Generate functionality

        self.content_stack.addWidget(self.manual_builder)  # Index 0
        self.content_stack.addWidget(self.sequence_generator)  # Index 1

        # Add widgets to the layout
        self.layout.addWidget(self.sequence_widget)
        self.layout.addWidget(self.content_stack)

        self.setLayout(self.layout)

    def show_build(self):
        """Display the Build (ManualBuilder) content."""
        self.content_stack.setCurrentWidget(self.manual_builder)

    def show_generate(self):
        """Display the Generate (SequenceGeneratorWidget) content."""
        self.content_stack.setCurrentWidget(self.sequence_generator)

    # def paintEvent(self, event):
    #     """Handle custom painting if necessary."""
    #     painter = QPainter(self)
    #     painter.save()
    #     try:
    #         # Custom painting logic here (if needed)
    #         pass  # Replace with actual painting code if needed
    #     finally:
    #         painter.restore()
    #     # No need to call painter.end()
