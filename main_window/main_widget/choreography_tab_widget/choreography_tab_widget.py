# choreography_tab_widget.py
from typing import TYPE_CHECKING, List, Dict
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter

from main_window.main_widget.choreography_tab_widget.music_player_widget import (
    MusicPlayerWidget,
)

from .timeline import Timeline
from ..sequence_dictionary_browser import SequenceDictionaryBrowser
from .annotation_editor import AnnotationEditor

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ChoreographyTabWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.timeline_widget = Timeline(self)
        self.dictionary_browser = SequenceDictionaryBrowser(self)
        self.annotation_editor = AnnotationEditor(self)
        self.music_player = MusicPlayerWidget(self)

    def _setup_layout(self):
        # Use a splitter to allow resizing between the dictionary and timeline
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.dictionary_browser)
        self.splitter.addWidget(self.timeline_widget)

        # Main layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)
        self.layout.addWidget(self.annotation_editor)
        self.layout.addWidget(self.music_player)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.timeline_widget.resize_timeline()
        self.dictionary_browser.resize_browser()
        self.annotation_editor.resize_editor()
