from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from typing import TYPE_CHECKING

from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.circular_auto_builder_frame import (
    CircularAutoBuilderFrame,
)
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.freeform_auto_builder_frame import (
    FreeformAutoBuilderFrame,
)


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
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)

        # Title for the AutoBuilder
        self.title_label = QLabel("Auto Builder")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.layout.addWidget(self.title_label)

        # Button layout
        button_layout = QHBoxLayout()

        # Freeform Builder Button
        self.freeform_button = QPushButton("Freeform Builder")
        self.freeform_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.freeform_button.clicked.connect(self.open_freeform_builder)
        button_layout.addWidget(self.freeform_button)

        # Circular Builder Button
        self.circular_button = QPushButton("Circular Builder")
        self.circular_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.circular_button.clicked.connect(self.open_circular_builder)
        button_layout.addWidget(self.circular_button)

        # Add button layout to the main layout
        self.layout.addLayout(button_layout)

        # Stacked widget to switch between builders
        self.builder_frame_container = QStackedWidget()
        self.layout.addWidget(self.builder_frame_container)

        # Create instances of the auto builder frames, but don't show them immediately
        self.freeform_builder_frame = FreeformAutoBuilderFrame(self)
        self.circular_builder_frame = CircularAutoBuilderFrame(self)

        # Add frames to the stacked widget
        self.builder_frame_container.addWidget(self.freeform_builder_frame)
        self.builder_frame_container.addWidget(self.circular_builder_frame)

    def open_freeform_builder(self):
        """Switch to Freeform Auto Builder."""
        self.builder_frame_container.setCurrentWidget(self.freeform_builder_frame)

    def open_circular_builder(self):
        """Switch to Circular Auto Builder."""
        self.builder_frame_container.setCurrentWidget(self.circular_builder_frame)

    def resize_auto_builder(self):
        """Resize handler for the auto builder UI."""
        # Add any resize logic for components here if needed.
        # resize the buttons
        button_font_size = self.width() // 50
        button_font = self.freeform_button.font()
        button_font.setPointSize(button_font_size)
        self.freeform_button.setFont(button_font)
        self.circular_button.setFont(button_font)
        # resize the title
        title_font_size = self.width() // 40
        title_font = self.title_label.font()
        title_font.setPointSize(title_font_size)
        self.title_label.setFont(title_font)
        # resize the builder frames
        self.freeform_builder_frame._resize_freeform_auto_builder_frame()
        self.circular_builder_frame._resize_circular_auto_builder_frame()
