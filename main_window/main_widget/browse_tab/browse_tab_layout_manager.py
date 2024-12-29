from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabLayoutManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.layout = QHBoxLayout(self.browse_tab)
        self.stacked_layout = QStackedLayout()
        self.main_content_widget = QWidget()

    def setup_layout(self):
        """Sets up the main layout structure using QStackedLayout."""
        self.browse_tab = self.browse_tab
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.browse_tab.setContentsMargins(0, 0, 0, 0)

        initial_layout = QVBoxLayout()
        initial_layout.addWidget(self.browse_tab.initial_selection_widget)

        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        self.main_content_layout.addWidget(self.browse_tab.go_back_button)
        self.main_content_layout.addWidget(self.browse_tab.currently_displaying_label)
        self.main_content_layout.addWidget(self.browse_tab.sequence_count_label)
        self.main_content_layout.addWidget(self.browse_tab.sort_widget)

        self.scroll_widget_container = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget_container)
        self.scroll_layout.addWidget(self.browse_tab.nav_sidebar, 1)
        self.scroll_layout.addWidget(self.browse_tab.scroll_widget, 9)
        self.main_content_layout.addWidget(self.scroll_widget_container)

        self.stacked_layout.addWidget(self.browse_tab.initial_selection_widget)
        self.stacked_layout.addWidget(self.main_content_widget)
        self.layout.addLayout(self.stacked_layout)
        self.stacked_layout.setCurrentIndex(0)

    def switch_to_main_content(self):
        """Switch to the main content page in the stacked layout."""
        self.browse_tab.go_back_button.show()
        self.browse_tab.preview_area.image_label.show()
        self.browse_tab.sequence_count_label.show()
        self.stacked_layout.setCurrentIndex(1)

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        self.stacked_layout.setCurrentIndex(0)
        preview_area = self.browse_tab.preview_area
        preview_area.word_label.setText("")
        self.browse_tab.initial_selection_widget.show()

        self.browse_tab.preview_area.clear_preview()
        self.browse_tab.sequence_count_label.hide()

        self.browse_tab.dictionary_settings.set_current_section("filter_choice")
        self.browse_tab.dictionary_settings.set_current_filter(None)
        self.browse_tab.initial_selection_widget.show_section("filter_choice")
