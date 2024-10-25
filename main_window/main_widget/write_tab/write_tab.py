# write_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter

from .timeline import Timeline
from ..sequence_dictionary_browser import SequenceDictionaryBrowser
from .annotation_editor import AnnotationEditor
from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
    SequenceWidgetBeatFrame,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


# write_tab.py


class WriteTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.timeline = Timeline(self)
        self.dictionary_browser = SequenceDictionaryBrowser(self)
        self.annotation_editor = AnnotationEditor(self)

        # Instantiate SequenceWidgetBeatFrame
        self.beat_frame = SequenceWidgetBeatFrame(self.main_widget)
        self.beat_frame._init_beats()  # Initialize beats

    def _setup_layout(self):
        # Use a splitter to allow resizing between the dictionary and timeline
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.dictionary_browser)
        self.splitter.addWidget(self.timeline)

        # Add beat frame to layout
        self.splitter.addWidget(self.beat_frame)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

        # Set the title and date after the layout has been set up
        self.timeline.header_widget.set_title("My Timeline Title")
        self.timeline.header_widget.set_date("2024-10-24")

    def resizeEvent(self, event):
        self.timeline.resize_timeline()
        self.dictionary_browser.resize_browser()
        self.annotation_editor.resize_editor()
        super().resizeEvent(event)
