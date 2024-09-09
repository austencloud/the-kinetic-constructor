from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer
from main_window.main_widget.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class FilterSectionBase(QWidget):
    def __init__(
        self,
        initial_selection_widget: "DictionaryInitialSelectionsWidget",
        label_text: str,
    ):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self.browser = initial_selection_widget.browser
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.section_manager = self.browser.section_manager
        self.main_widget = initial_selection_widget.browser.main_widget
        self.metadata_extractor = self.main_widget.metadata_extractor
        self._setup_ui(label_text)
        self._initialize_progress_bar()
        self.initialized = False

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        # Create a top bar with the back button on the left
        top_bar_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(
            self.initial_selection_widget.show_filter_choice_widget
        )
        top_bar_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        # Add the label centered below the top bar
        self.header_label = QLabel(label_text)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        layout.addStretch(1)
        # Set the layout
        self.setLayout(layout)

        self.back_button.hide()
        self.header_label.hide()

    def _initialize_progress_bar(self):
        # Initialize the custom rainbow progress bar
        self.progress_bar = RainbowProgressBar(
            self.browser.scroll_widget.scroll_content
        )
        self.progress_bar.setVisible(False)

    def _style_progress_bar(self):
        self.progress_bar.setFixedWidth(self.browser.width() // 3)
        self.progress_bar.setFixedHeight(self.browser.height() // 6)

        # Update the font to Monotype Corsiva
        progress_bar_font = self.progress_bar.percentage_label.font()
        progress_bar_font.setFamily("Monotype Corsiva")  # Set font to Monotype Corsiva
        progress_bar_font.setPointSize(self.browser.width() // 40)
        self.progress_bar.percentage_label.setFont(progress_bar_font)
        self.progress_bar.loading_label.setFont(progress_bar_font)

    def _prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browser.currently_displaying_label.show_loading_message(description)
        self.browser.number_of_currently_displayed_words_label.setText("")
        self.browser.scroll_widget.clear_layout()
        self.browser.scroll_widget.grid_layout.addWidget(
            self.progress_bar,
            0,
            0,
            1,
            self.thumbnail_box_sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self._style_progress_bar()
        self.progress_bar.setVisible(True)
        QApplication.processEvents()

    def _update_and_display_ui(
        self, filter_description_prefix, total_sequences: int, filter_description: str
    ):
        if total_sequences == 0:
            total_sequences = 1  # Prevent division by zero

        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words to be displayed: {total_sequences}"
        )

        def update_ui():
            num_words = 0
            nonlocal filter_description_prefix
            nonlocal filter_description
            for index, (word, thumbnails, _) in enumerate(
                self.browser.currently_displayed_sequences
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
                self.browser.number_of_currently_displayed_words_label.setText(
                    f"Number of words: {num_words}"
                )
                QApplication.processEvents()

            self.progress_bar.setVisible(False)
            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
            )
            if filter_description_prefix == "level":
                filter_description = f"level {filter_description} sequences"
                filter_description_prefix = ""
            self.browser.currently_displaying_label.show_completed_message(
                filter_description_prefix, filter_description
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)

    def add_buttons(self):
        # placeholder method, implemented in subclasses
        pass

    def resize_go_back_button(self):
        self.back_button.setFixedWidth(self.browser.width() // 10)
        self.back_button.setFixedHeight(self.browser.height() // 20)
        font = self.back_button.font()
        font.setPointSize(self.browser.height() // 80)
        self.back_button.setFont(font)
        QApplication.processEvents()
