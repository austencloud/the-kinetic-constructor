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
from widgets.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
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

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        # Create a top bar with the back button on the left
        top_bar_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(
            self.initial_selection_widget.show_filter_choice_widget
        )
        top_bar_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        # Add the label centered below the top bar
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addStretch(1)
        # Set the layout
        self.setLayout(layout)

    def _initialize_progress_bar(self):
        # Initialize the custom rainbow progress bar
        self.loading_progress_bar = RainbowProgressBar(
            self.browser.scroll_widget.scroll_content
        )
        self.loading_progress_bar.setVisible(False)

    def _style_loading_bar(self):
        self.loading_progress_bar.setFixedWidth(self.browser.width() // 3)
        self.loading_progress_bar.setFixedHeight(self.browser.height() // 10)

        # Update the font to Monotype Corsiva
        loading_bar_font = self.loading_progress_bar.percentage_label.font()
        loading_bar_font.setFamily("Monotype Corsiva")  # Set font to Monotype Corsiva
        loading_bar_font.setPointSize(self.browser.width() // 40)
        self.loading_progress_bar.percentage_label.setFont(loading_bar_font)

    def _prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browser.currently_displaying_label.show_loading_message(description)
        self.browser.number_of_currently_displayed_words_label.setText("")
        self.browser.scroll_widget.clear_layout()
        self.browser.scroll_widget.grid_layout.addWidget(
            self.loading_progress_bar,
            0,
            0,
            1,
            self.thumbnail_box_sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self._style_loading_bar()
        self.loading_progress_bar.setVisible(True)
        QApplication.processEvents()

    def _update_and_display_ui(self, total_sequences: int, filter_description: str):
        if total_sequences == 0:
            total_sequences = 1  # Prevent division by zero

        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words to be displayed: {total_sequences}"
        )

        def update_ui():
            num_words = 0

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
                self.loading_progress_bar.setValue(percentage)
                self.browser.number_of_currently_displayed_words_label.setText(
                    f"Number of words displayed: {num_words}"
                )
                QApplication.processEvents()

            self.loading_progress_bar.setVisible(False)
            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
            )

            self.browser.currently_displaying_label.show_completed_message(
                filter_description
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)
