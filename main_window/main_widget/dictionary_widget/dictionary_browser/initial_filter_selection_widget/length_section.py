from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LengthSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Sequence Length:")
        self.initialized = False

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.header_label.show()
        layout: QVBoxLayout = self.layout()

        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for length in available_lengths:
            button = QPushButton(str(length))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"length_{length}"] = button
            button.clicked.connect(
                lambda checked, l=length: self.initial_selection_widget.on_length_button_clicked(
                    l
                )
            )
            vbox.addWidget(button)

        layout.addLayout(vbox)
        layout.addStretch(1)
        self.resize_length_section()

    def display_only_thumbnails_with_sequence_length(self, length: str):
        self.initial_selection_widget.browser.dictionary_widget.dictionary_settings.set_current_filter(
            {"length": length}
        )
        self._prepare_ui_for_filtering(f"sequences of length {length}")

        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        total_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if seq_length != length:
                continue

            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )
            total_sequences += 1

        self._update_and_display_ui(" sequences of length", total_sequences, length)


    def resize_length_section(self):
        self.resize_buttons()
        self.resize_label()

    def resize_label(self):
        font = self.header_label.font()
        font.setPointSize(self.main_widget.width() // 100)
        self.header_label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.main_widget.width() // 100)
            button.setFont(font)
            button.setFixedHeight(self.main_widget.height() // 20)
            button.setFixedWidth(self.main_widget.width() // 8)
