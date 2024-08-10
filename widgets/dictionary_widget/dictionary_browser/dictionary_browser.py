from typing import TYPE_CHECKING

from widgets.dictionary_widget.dictionary_browser.dictionary_nav_sidebar import (
    DictionaryNavSidebar,
)
from widgets.dictionary_widget.dictionary_sorter import DictionarySorter
from .browser_scroll_widget import DictionaryBrowserScrollWidget

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from widgets.dictionary_widget.dictionary_options_widget import (
    DictionaryOptionsWidget,
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
        self.sidebar = DictionaryNavSidebar(self)
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.options_widget = DictionaryOptionsWidget(self)
        self.sorter = DictionarySorter(self)
        sort_method = (
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
        self.sorter.sort_and_display_thumbnails(sort_method)
        

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_layout = QHBoxLayout()

        self.layout.addWidget(self.options_widget)
        self.scroll_layout.addWidget(self.sidebar, 1)
        self.scroll_layout.addWidget(self.scroll_widget, 9)

        self.layout.addLayout(self.scroll_layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def resize_dictionary_browser(self):
        self.scroll_widget.resize_dictionary_browser_scroll_widget()
