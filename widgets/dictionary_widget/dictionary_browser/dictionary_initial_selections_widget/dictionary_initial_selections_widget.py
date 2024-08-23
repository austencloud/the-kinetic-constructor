from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.author_section import (
    AuthorSection,
)
from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.filter_choice_widget import (
    FilterChoiceWidget,
)
from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.filter_section_base import (
    FilterSectionBase,
)

from .contains_letter_section import ContainsLetterSection
from .length_section import LengthSection
from .level_section import LevelSection
from .starting_letter_section import StartingLetterSection
from .starting_position_section import StartingPositionSection

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryInitialSelectionsWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.browser = browser
        self.selected_letters: set[str] = set()

        # Initialize sections
        self.starting_letter_section = StartingLetterSection(self)
        self.contains_letter_section = ContainsLetterSection(self)
        self.length_section = LengthSection(self)
        self.level_section = LevelSection(self)
        self.starting_position_section = StartingPositionSection(self)
        self.author_section = AuthorSection(self)  # Initialize AuthorSection

        self.sections: list[FilterSectionBase] = [
            self.starting_letter_section,
            self.length_section,
            self.level_section,
            self.contains_letter_section,
            self.starting_position_section,
            self.author_section,
        ]
        self.filter_choice_widget = FilterChoiceWidget(self)

        self._setup_ui()

    def show_author_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.author_section.show()
        self.main_layout.addWidget(self.author_section)

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.filter_choice_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def show_filter_choice_widget(self):
        """Show the filter choice widget and hide any active section."""
        self._hide_all_sections()
        self.filter_choice_widget.show()

    def _hide_all_sections(self):
        """Hide all filter sections."""
        self.starting_letter_section.hide()
        self.contains_letter_section.hide()
        self.length_section.hide()
        self.level_section.hide()
        self.starting_position_section.hide()
        self.author_section.hide()  # Hide the AuthorSection

    def show_starting_letter_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.starting_letter_section.show()
        self.main_layout.addWidget(self.starting_letter_section)

    def show_contains_letter_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.contains_letter_section.show()
        self.main_layout.addWidget(self.contains_letter_section)

    def show_length_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.length_section.show()
        self.main_layout.addWidget(self.length_section)

    def show_level_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.level_section.show()
        self.main_layout.addWidget(self.level_section)
        self.level_section.resize_level_section()

    def show_starting_position_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.starting_position_section.show()
        self.main_layout.addWidget(self.starting_position_section)

    def on_letter_button_clicked(self, letter: str):
        self.browser.apply_initial_selection({"letter": letter})
        self.show_filter_choice_widget()

    def on_length_button_clicked(self, length: int):
        self.browser.apply_initial_selection({"length": length})
        self.show_filter_choice_widget()

    def on_level_button_clicked(self, level: int):
        self.browser.apply_initial_selection({"level": level})
        self.show_filter_choice_widget()

    def on_contains_letter_button_clicked(self, letter: str):
        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
        else:
            self.selected_letters.add(letter)

    def on_position_button_clicked(self, position: str):
        self.browser.apply_initial_selection({"position": position})
        self.show_filter_choice_widget()

    def on_author_button_clicked(self, author: str):
        self.browser.apply_initial_selection({"author": author})
        self.show_filter_choice_widget()

    def apply_contains_letter_filter(self):
        self.browser.apply_initial_selection(
            {"contains_letters": self.selected_letters}
        )
        self.show_filter_choice_widget()

    def resize_initial_selections_widget(self):
        self.resize_initial_filter_buttons()
        self.resize_fonts_in_each_section()
        self.resize_buttons_in_each_section()
        self.filter_choice_widget.resize_filter_choice_widget()
        for section in self.sections:
            section.resize_go_back_button()

    def resize_initial_filter_buttons(self):
        for button in self.filter_choice_widget.buttons.values():
            button.setFixedWidth(self.browser.width() // 5)

    def resize_fonts_in_each_section(self):
        for section in self.sections:
            self._resize_labels(section.label)

    def resize_buttons_in_each_section(self):
        for section in self.sections:
            for button in section.buttons.values():
                self._resize_buttons(button)

    def _resize_buttons(self, button: QPushButton):
        font = button.font()
        font.setPointSize(self.browser.width() // 100)
        button.setFont(font)

    def _resize_labels(self, label: QLabel):
        font = label.font()
        font.setPointSize(self.browser.width() // 100)
        label.setFont(font)
        for button in self.filter_choice_widget.buttons.values():
            button.setFont(font)
