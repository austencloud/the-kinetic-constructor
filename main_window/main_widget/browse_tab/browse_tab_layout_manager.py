from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout

if TYPE_CHECKING:
    from .browse_tab import BrowseTab


class BrowseTabLayoutManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.main_widget = self.browse_tab.main_widget
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
        # initial_layout.addWidget(self.browse_tab.initial_selection_widget)

        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        self.main_content_layout.addWidget(self.browse_tab.go_back_button)

        # self.stacked_layout.addWidget(self.browse_tab.initial_selection_widget)

        self.layout.addLayout(self.stacked_layout)
        self.stacked_layout.setCurrentIndex(0)

    def switch_to_sequence_picker(self):
        """Switch to the main content page in the stacked layout."""
        self.browse_tab.go_back_button.show()
        self.browse_tab.sequence_viewer.image_label.show()
        self.main_widget.fade_manager.fade_to_tab(
            self.main_widget.left_stack,
            self.main_widget.left_sequence_picker_index,
        )

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        self.stacked_layout.setCurrentIndex(0)
        preview_area = self.browse_tab.sequence_viewer
        preview_area.word_label.setText("")
        self.main_widget.fade_manager.fade_to_tab(
            self.main_widget.left_stack,
            self.main_widget.left_filter_selector_index,
        )

        self.browse_tab.sequence_viewer.clear()
        self.browse_tab.browse_tab_settings.set_current_section("filter_choice")
        self.browse_tab.browse_tab_settings.set_current_filter(None)
        self.browse_tab.sequence_picker.filter_selector.show_section("filter_choice")
