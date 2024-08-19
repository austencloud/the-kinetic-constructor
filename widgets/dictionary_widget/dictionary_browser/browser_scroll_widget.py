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

        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidget(self.scroll_content)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background: transparent;")
        self.thumbnail_boxes: list[ThumbnailBox] = []
        self.is_initialized = True
        self.section_headers: dict[int, "SectionHeader"] = {}

    def _remove_spacing(self):
        self.grid_layout.setSpacing(0)
        self.layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def display_loading_thumbnails_animated_text(self):
        self.loading_thumbnails_label = QLabel("Loading thumbnails...")
        self.loading_thumbnails_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.loading_thumbnails_label.font()
        font.setPointSize(self.width() // 30)
        self.loading_thumbnails_label.setFont(font)
        self.clear_layout()
        self.grid_layout.addWidget(self.loading_thumbnails_label, 0, 0)

        self.loading_animation_timer = QTimer(self)
        self.loading_animation_timer.timeout.connect(
            self.update_loading_thumbnails_text
        )
        self.loading_animation_timer.start(500)  # Change the interval as desired

    def update_loading_thumbnails_text(self):
        if not self.loading_thumbnails_label:
            return
        current_text = self.loading_thumbnails_label.text()
        if current_text.endswith("..."):
            new_text = "Loading thumbnails."
        elif current_text.endswith(".."):
            new_text = "Loading thumbnails..."
        else:
            new_text = "Loading thumbnails.."
        self.loading_thumbnails_label.setText(new_text)

    def remove_loading_thumbnails_text(self):
        self.loading_thumbnails_label.deleteLater()
        self.loading_animation_timer.stop()

    def clear_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)  # Ensure widgets are properly deleted

    def resize_dictionary_browser_scroll_widget(self):
        if self.is_initialized:
            thumbnail_boxes: list[ThumbnailBox] = self.thumbnail_boxes_dict.values()
            for box in thumbnail_boxes:
                box.resize_thumbnail_box()

    def show_variations(self, base_word):
        print(f"Show variations for {base_word}")

    def get_scrollbar_width(self):
        style = self.scroll_area.style()
        return style.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)

    def update_thumbnail_sizes(self):
        for box in self.thumbnail_boxes:
            box.resize_thumbnail_box()

    def find_insert_index(self, new_word):
        for i, box in enumerate(self.thumbnail_boxes):
            if box.word.lower() > new_word.lower():
                return i
        return len(self.thumbnail_boxes)

    def update_all_thumbnails(self):
        for thumbnail_box in self.thumbnail_boxes_dict.values():
            thumbnail_box.image_label.update_thumbnail()
