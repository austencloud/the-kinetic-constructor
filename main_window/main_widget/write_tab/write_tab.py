# write_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea

from .timeline import Timeline
from ..sequence_dictionary_browser import SequenceDictionaryBrowser
from .annotation_editor import AnnotationEditor
from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
    SequenceWidgetBeatFrame,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


from .act_beat_frame import ActBeatFrame


class WriteTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):

        # Use ActBeatFrame instead of rows of beats
        self.beat_frame = ActBeatFrame(self)
        self.beat_frame.init_act(
            num_beats=8, num_rows=10
        )  # Example: 8 beats per row, 10 rows

        self.timeline = Timeline(self)
        self.dictionary_browser = SequenceDictionaryBrowser(self)
        self.annotation_editor = AnnotationEditor(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.beat_frame)
        self.scroll_area.setWidgetResizable(True)

    def _setup_layout(self):
        # Use a splitter to allow resizing between the dictionary and timeline
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.dictionary_browser)
        self.splitter.addWidget(self.timeline)
        # self.splitter.addWidget(self.scroll_area)  # Wrap beat_frame in a scroll area

        # Add stretch factors to the widgets in the splitter
        self.splitter.setStretchFactor(0, 1)  # Smaller stretch for dictionary browser
        self.splitter.setStretchFactor(1, 2)  # Larger stretch for the beat frame (2/3 window)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)


        self.timeline.header_widget.set_title("My Timeline Title")
        self.timeline.header_widget.set_date("2024-10-24")

    def resizeEvent(self, event):
        self.timeline.resize_timeline()
        self.dictionary_browser.resize_browser()
        self.annotation_editor.resize_editor()
        super().resizeEvent(event)
