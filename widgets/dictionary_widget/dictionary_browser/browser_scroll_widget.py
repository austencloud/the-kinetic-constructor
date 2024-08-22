from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QTimer

from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QStyle,
    QLabel,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )
    from widgets.dictionary_widget.dictionary_browser.section_header import (
        SectionHeader,
    )


class DictionaryBrowserScrollWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.is_initialized = False
        self.browser = browser
        self.thumbnail_boxes_dict: dict[str, ThumbnailBox] = {}
        self.scroll_content = QWidget()
        self.setStyleSheet("background: transparent;")
        self.thumbnail_boxes: list[ThumbnailBox] = []
        self.is_initialized = True
        self.section_headers: dict[int, "SectionHeader"] = {}
        self._setup_scroll_area()
        self._setup_layout()


    def _setup_layout(self):
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def _setup_scroll_area(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidget(self.scroll_content)

    def clear_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def resize_dictionary_browser_scroll_widget(self):
        if self.is_initialized:
            thumbnail_boxes: list[ThumbnailBox] = self.thumbnail_boxes_dict.values()
            for box in thumbnail_boxes:
                box.resize_thumbnail_box()


