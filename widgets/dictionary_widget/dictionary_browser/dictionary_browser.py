from typing import TYPE_CHECKING
from .browser_scroll_widget import DictionaryBrowserScrollWidget

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from widgets.dictionary_widget.dictionary_sorter import (
    DictionarySorter,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryBrowser(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.dictionary_widget = dictionary_widget
        self.main_widget = dictionary_widget.main_widget

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.sorter = DictionarySorter(self)
        self.sorter.sort_and_display_thumbnails()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.sorter)
        self.layout.addWidget(self.scroll_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def resize_dictionary_browser(self):
        self.scroll_widget.resize_dictionary_browser_scroll_widget()

    def showEvent(self, event):
        super().showEvent(event)
        # Update all thumbnail images when the widget is shown

