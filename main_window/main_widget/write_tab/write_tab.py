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
        self.beat_frame = ActBeatFrame(self)
        self.beat_frame.init_act(num_beats=8, num_rows=10)

        self.timeline = Timeline(self)
        self.dictionary_browser = SequenceDictionaryBrowser(self)

    def _setup_layout(self):
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.dictionary_browser)
        self.splitter.addWidget(self.timeline)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.setStyleSheet("background-color: rgba(255, 255, 255, 140);")



    def resizeEvent(self, event):
        self.timeline.resize_timeline()
        self.dictionary_browser.resize_browser()
        super().resizeEvent(event)
