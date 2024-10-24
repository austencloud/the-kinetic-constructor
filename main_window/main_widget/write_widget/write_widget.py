# write_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter

from .timeline import Timeline
from ..sequence_dictionary_browser import SequenceDictionaryBrowser
from .annotation_editor import AnnotationEditor

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class WriteWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.timeline_widget = Timeline(self)
        self.dictionary_browser = SequenceDictionaryBrowser(self)
        self.annotation_editor = AnnotationEditor(self)

    def _setup_layout(self):
        # Use a splitter to allow resizing between the dictionary and timeline
        self.splitter = QSplitter(self)
        self.splitter.addWidget(self.dictionary_browser)
        self.splitter.addWidget(self.timeline_widget)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.timeline_widget.resize_timeline()
        self.dictionary_browser.resize_browser()
        self.annotation_editor.resize_editor()
        super().resizeEvent(event)
