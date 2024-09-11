from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.author_section import (
    AuthorSection,
)
from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.filter_choice_widget import (
    FilterChoiceWidget,
)
from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.filter_section_base import (
    FilterSectionBase,
)

from .contains_letter_section import ContainsLetterSection
from .length_section import LengthSection
from .level_section import LevelSection
from .starting_letter_section import StartingLetterSection
from .starting_position_section import StartingPositionSection

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
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
        self.author_section = AuthorSection(self)

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

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.filter_choice_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        current_section = (
            self.browser.dictionary_widget.dictionary_settings.get_current_section()
        )
        section_map = {
            "filter_choice": self.show_filter_choice_widget,
            "starting_letter": self.show_starting_letter_section,
            "contains_letter": self.show_contains_letter_section,
            "length": self.show_length_section,
            "level": self.show_level_section,
            "starting_position": self.show_starting_position_section,
            "author": self.show_author_section,
        }

        if current_section in section_map:
            section_map[current_section]()

    def show_filter_choice_widget(self):
        """Show the filter choice widget and hide any active section."""
        self._hide_all_sections()
        self.filter_choice_widget.show()
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "filter_choice"
        )

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
        if not self.starting_letter_section.initialized:
            self.starting_letter_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "starting_letter"
        )
        self.starting_letter_section.resize_starting_letter_section()

    def show_contains_letter_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.contains_letter_section.show()
        self.main_layout.addWidget(self.contains_letter_section)
        if not self.contains_letter_section.initialized:
            self.contains_letter_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "contains_letter"
        )

    def show_length_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.length_section.show()
        self.main_layout.addWidget(self.length_section)
        if not self.length_section.initialized:
            self.length_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section("length")

    def show_level_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.level_section.show()
        self.main_layout.addWidget(self.level_section)
        if not self.level_section.initialized:
            self.level_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section("level")

    def show_starting_position_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.starting_position_section.show()
        self.main_layout.addWidget(self.starting_position_section)
        if not self.starting_position_section.initialized:
            self.starting_position_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "starting_position"
        )

    def show_author_section(self):
        self._hide_all_sections()
        self.filter_choice_widget.hide()
        self.author_section.show()
        self.main_layout.addWidget(self.author_section)
        if not self.author_section.initialized:
            self.author_section.add_buttons()
        self.browser.dictionary_widget.dictionary_settings.set_current_section("author")

    def on_letter_button_clicked(self, letter: str):
        self.browser.apply_current_filter({"letter": letter})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def on_length_button_clicked(self, length: int):
        self.browser.apply_current_filter({"length": length})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def on_level_button_clicked(self, level: int):
        self.browser.apply_current_filter({"level": level})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def on_contains_letter_button_clicked(self, letter: str):
        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
        else:
            self.selected_letters.add(letter)

    def on_position_button_clicked(self, position: str):
        self.browser.apply_current_filter({"position": position})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def on_author_button_clicked(self, author: str):
        self.browser.apply_current_filter({"author": author})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def apply_contains_letter_filter(self):
        self.browser.apply_current_filter({"contains_letters": self.selected_letters})
        self.browser.dictionary_widget.dictionary_settings.set_current_section(
            "browser"
        )

    def resize_initial_selections_widget(self):
        self.resize_initial_filter_buttons()
        self.filter_choice_widget.resize_filter_choice_widget()
        for section in self.sections:
            section.resize_go_back_button()

    def resize_initial_filter_buttons(self):
        for button in self.filter_choice_widget.buttons.values():
            button.setFixedWidth(self.browser.width() // 5)
