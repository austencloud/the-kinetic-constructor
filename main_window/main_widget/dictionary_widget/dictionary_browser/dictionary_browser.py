from datetime import datetime
import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer

from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_progress_bar import (
    DictionaryProgressBar,
)
from .initial_filter_selection_widget.dictionary_initial_selections_widget import (
    DictionaryInitialSelectionsWidget,
)

# from .video_preview_widget import VideoPreviewWidget
from utilities.path_helpers import get_images_and_data_path
from .currently_displaying_indicator_label import CurrentlyDisplayingIndicatorLabel
from .dictionary_browser_nav_sidebar import DictionaryBrowserNavSidebar
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QApplication
from .dictionary_browser_section_manager import SectionManager

from .thumbnail_box_sorter import ThumbnailBoxSorter
from .dictionary_browser_scroll_widget import DictionaryBrowserScrollWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from .dictionary_browser_options_panel.dictionary_browser_options_panel import (
    DictionaryOptionsPanel,
)
from PyQt6.QtWidgets import QLabel

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import (
        DictionaryWidget,
    )


class DictionaryBrowser(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.dictionary_widget = dictionary_widget
        self.main_widget = dictionary_widget.main_widget
        self.initialized = False
        self.currently_displayed_sequences = []
        self.num_columns = 3
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.setup_components()
        self.initial_selection_widget = DictionaryInitialSelectionsWidget(self)

    def setup_components(self):
        self.currently_displaying_label = CurrentlyDisplayingIndicatorLabel(self)
        self.nav_sidebar = DictionaryBrowserNavSidebar(self)
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.section_manager = SectionManager(self)
        self.thumbnail_box_sorter = ThumbnailBoxSorter(self)
        self.options_widget = DictionaryOptionsPanel(self)
        # self.video_preview_widget = VideoPreviewWidget(self)

        self._setup_go_back_to_initial_selection_widget_button()
        self._setup_number_of_currently_displayed_sequences_label()
        self.widgets: list[QWidget] = [
            self.nav_sidebar,
            self.scroll_widget,
            self.options_widget,
            self.back_button,
            self.currently_displaying_label,
            self.number_of_sequences_label,
        ]
        for widget in self.widgets:
            widget.hide()
        self._initialize_progress_bar()

    def prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.currently_displaying_label.setText("")
        QApplication.processEvents()
        self.currently_displaying_label.show_message(description)
        self.number_of_sequences_label.setText("")
        self.scroll_widget.clear_layout()
        self.scroll_widget.grid_layout.addWidget(
            self.progress_bar,
            0,
            0,
            1,
            self.thumbnail_box_sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.progress_bar._style_dictionary_progress_bar()
        self.progress_bar.setVisible(True)
        QApplication.processEvents()

    def _initialize_progress_bar(self):
        self.progress_bar = DictionaryProgressBar(self.scroll_widget.scroll_content)
        self.progress_bar.setVisible(False)

    def _setup_number_of_currently_displayed_sequences_label(self):
        self.number_of_sequences_label = QLabel("")
        self.number_of_sequences_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_go_back_to_initial_selection_widget_button(self):
        self.back_button = QPushButton("Back")
        self.go_back_button_layout = QHBoxLayout()
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_back_button_layout.addWidget(self.back_button)
        self.go_back_button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.back_button.clicked.connect(self.go_back_to_initial_selection_widget)

    def go_back_to_initial_selection_widget(self):
        for widget in self.widgets:
            widget.hide()
        self.initial_selection_widget.show()
        self.dictionary_widget.preview_area.hide()
        self.dictionary_widget.preview_area.clear_preview()
        self.number_of_sequences_label.hide()
        self.dictionary_widget.dictionary_settings.set_current_section("filter_choice")
        self.dictionary_widget.dictionary_settings.set_current_filter(None)
        self.initial_selection_widget.show_section("filter_choice")

    def add_initial_selection_widget(self):
        self.layout.addWidget(self.initial_selection_widget)

    def apply_current_filter(self, current_filter):
        self.current_filter = current_filter
        self.initial_selection_widget.hide()
        self._add_components_to_layout()
        self._initialize_and_sort_thumbnails(current_filter)
        self.dictionary_widget.preview_area.update_preview(None)
        QApplication.processEvents()

    def _initialize_and_sort_thumbnails(self, current_filter):
        self.thumbnail_box_sorter.sort_and_display_thumbnail_boxes_by_current_filter(
            current_filter
        )
        self.initialized = True

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_widget_container = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget_container)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.initial_selection_widget)
        # self.layout.addWidget(self.video_preview_widget)

    def _add_components_to_layout(self):
        self.layout.addLayout(self.go_back_button_layout)
        self.layout.addWidget(self.currently_displaying_label)
        self.layout.addWidget(self.number_of_sequences_label)
        self.layout.addWidget(self.options_widget)
        self.layout.addWidget(self.scroll_widget)
        self.scroll_layout.addWidget(self.nav_sidebar, 1)
        self.scroll_layout.addWidget(self.scroll_widget, 9)
        self.layout.addWidget(self.scroll_widget_container)
        self.dictionary_widget.layout.addWidget(self.dictionary_widget.preview_area, 3)
        for widget in self.widgets:
            widget.show()
        self.dictionary_widget.preview_area.show()
        self.resize_currently_displaying_label()
        self.resize_number_of_currently_displayed_sequences_label()

    def resize_dictionary_browser(self):
        self.scroll_widget.resize_dictionary_browser_scroll_widget()
        self.resize_go_back_button()
        self.resize_currently_displaying_label()
        self.resize_number_of_currently_displayed_sequences_label()
        self.initial_selection_widget.resize_initial_selections_widget()
        self.nav_sidebar.resize_nav_sidebar()

    def resize_number_of_currently_displayed_sequences_label(self):
        font = self.number_of_sequences_label.font()
        font.setPointSize(self.width() // 80)
        self.number_of_sequences_label.setFont(font)

    def resize_go_back_button(self):
        self.back_button.setFixedWidth(self.main_widget.width() // 20)
        self.back_button.setFixedHeight(self.main_widget.height() // 20)
        font = self.back_button.font()
        font.setPointSize(self.main_widget.width() // 120)
        self.back_button.setFont(font)

    def resize_currently_displaying_label(self):
        font = self.currently_displaying_label.font()
        font.setPointSize(self.width() // 65)
        self.currently_displaying_label.setFont(font)

    def reset_filters(self):
        """Reset filters and display all sequences."""
        self._initialize_and_sort_thumbnails(
            self.main_widget.main_window.settings_manager.dictionary_settings.get_sort_method()
        )

    def show_browser_with_filters_from_settings(self):
        """Show browser with filters from settings."""
        current_filter = (
            self.main_widget.main_window.settings_manager.dictionary_settings.get_current_filter()
        )

        self.apply_current_filter(current_filter)

    def load_sequence_with_video(self, metadata: dict):
        video_url = metadata.get("video_url")
        if video_url:
            self.video_preview_widget.load_video(video_url)
            self.video_preview_widget.show()
        else:
            self.video_preview_widget.hide()  # Hide if no video available

    def show_favorites(self):
        """Show only favorite sequences."""

        self.prepare_ui_for_filtering(f"favorite sequences")
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (
                word,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]

        favorites = []
        for word, thumbnails in base_words:
            for thumbnail in thumbnails:
                if self.main_widget.metadata_extractor.get_favorite_status(thumbnail):
                    sequence_length = (
                        self.main_widget.metadata_extractor.get_sequence_length(
                            thumbnail
                        )
                    )
                    favorites.append((word, thumbnails, sequence_length))
                    break

        self.currently_displayed_sequences = favorites
        self.update_and_display_ui(len(favorites), "favorite sequences")

    def show_all_sequences(self):
        """Show all sequences."""
        self.prepare_ui_for_filtering(f"all sequences")

        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (
                word,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]
        sequences = []
        for word, thumbnails in base_words:
            for thumbnail in thumbnails:
                sequence_length = (
                    self.main_widget.metadata_extractor.get_sequence_length(thumbnail)
                )
                sequences.append((word, thumbnails, sequence_length))
        self.currently_displayed_sequences = sequences

        self.update_and_display_ui(len(sequences), "all sequences")

    def show_most_recent_sequences(self, date: datetime):
        self.prepare_ui_for_filtering(f"most recent sequences")
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (
                word,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]
        most_recent = []
        for word, thumbnails in base_words:
            date_added = self.section_manager.get_date_added(thumbnails)
            if date_added and date_added >= date:
                sequence_length = (
                    self.main_widget.metadata_extractor.get_sequence_length(
                        thumbnails[0]
                    )
                )
                most_recent.append((word, thumbnails, sequence_length))
                # break

        self.currently_displayed_sequences = most_recent
        self.update_and_display_ui(len(most_recent), "most recent sequences")

    def update_and_display_ui(self, total_sequences: int, filter_description: str):
        if total_sequences == 0:
            total_sequences = 1  # Prevent division by zero

        self.number_of_sequences_label.setText(
            f"Number of words to be displayed: {total_sequences}"
        )

        def update_ui():
            num_words = 0
            nonlocal filter_description
            for index, (word, thumbnails, _) in enumerate(
                self.currently_displayed_sequences
            ):
                row_index = index // self.thumbnail_box_sorter.num_columns
                column_index = index % self.thumbnail_box_sorter.num_columns
                self.thumbnail_box_sorter.add_thumbnail_box(
                    row_index=row_index,
                    column_index=column_index,
                    word=word,
                    thumbnails=thumbnails,
                    hidden=True,
                )
                num_words += 1

                percentage = int((num_words / total_sequences) * 100)
                self.progress_bar.setValue(percentage)
                self.number_of_sequences_label.setText(f"Number of words: {num_words}")
                QApplication.processEvents()

            self.progress_bar.setVisible(False)
            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                self.main_widget.main_window.settings_manager.dictionary_settings.get_sort_method()
            )
            font_color = self.main_widget.main_window.settings_manager.global_settings.font_color_updater.get_font_color(
                self.main_widget.main_window.settings_manager.global_settings.get_background_type()
            )
            for thumbnail_box in self.scroll_widget.thumbnail_boxes.values():
                thumbnail_box.word_label.setStyleSheet(f"color: {font_color};")
                if font_color == "white":
                    thumbnail_box.word_label.star_icon_empty_path = (
                        "star_empty_white.png"
                    )
                elif font_color == "black":
                    thumbnail_box.word_label.star_icon_empty_path = (
                        "star_empty_black.png"
                    )
                # reload the QIcons with the path
                thumbnail_box.word_label.reload_favorite_icon()
                thumbnail_box.variation_number_label.setStyleSheet(
                    f"color: {font_color};"
                )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)

    def get_all_sequences(self):
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (
                word,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, word)
                ),
            )
            for word in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, word))
            and "__pycache__" not in word
        ]
        sequences = []
        for word, thumbnails in base_words:
            for thumbnail in thumbnails:
                sequence_length = (
                    self.main_widget.metadata_extractor.get_sequence_length(thumbnail)
                )
                sequences.append((word, thumbnails, sequence_length))
        return sequences
