from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt

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
        self.buttons: dict[str, QPushButton] = {}
        self.selected_letters: set[str] = set()

        # Initialize sections
        self.starting_letter_section = StartingLetterSection(self)
        self.contains_letter_section = ContainsLetterSection(self)
        self.length_section = LengthSection(self)
        self.level_section = LevelSection(self)
        self.starting_position_section = StartingPositionSection(self)

        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.starting_letter_section)
        layout.addWidget(self.contains_letter_section)
        layout.addWidget(self.length_section)
        layout.addWidget(self.level_section)
        layout.addWidget(self.starting_position_section)  # New section
        self.setLayout(layout)

    def on_letter_button_clicked(self, letter: str):
        self.browser.apply_initial_selection({"letter": letter})

    def on_length_button_clicked(self, length: int):
        self.browser.apply_initial_selection({"length": length})

    def on_level_button_clicked(self, level: int):
        self.browser.apply_initial_selection({"level": level})

    def on_contains_letter_button_clicked(self, letter: str):
        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
        else:
            self.selected_letters.add(letter)

    def on_position_button_clicked(self, position: str):
        self.browser.apply_initial_selection({"position": position})

    def apply_contains_letter_filter(self):
        self.browser.apply_initial_selection(
            {"contains_letters": self.selected_letters}
        )

    def resizeEvent(self, event):
        self.resize_fonts_in_each_section()
        self.resize_buttons_in_each_section()
        super().resizeEvent(event)

    def resize_fonts_in_each_section(self):
        self._resize_labels(self.starting_letter_section.starting_letter_label)
        self._resize_labels(self.length_section.length_label)
        self._resize_labels(self.level_section.level_label)
        self._resize_labels(self.contains_letter_section.contains_letter_label)
        self._resize_labels(self.starting_position_section.starting_position_label)

    def resize_buttons_in_each_section(self):
        for button in self.starting_letter_section.buttons.values():
            self._resize_buttons(button)
        for button in self.length_section.buttons.values():
            self._resize_buttons(button)
        for button in self.level_section.buttons.values():
            self._resize_buttons(button)
        for button in self.contains_letter_section.buttons.values():
            self._resize_buttons(button)
        for button in self.starting_position_section.buttons.values():
            self._resize_buttons(button)

    def _resize_buttons(self, button: QPushButton):
        font = button.font()
        font.setPointSize(self.browser.width() // 100)
        button.setFont(font)

    def _resize_labels(self, label: QLabel):
        font = label.font()
        font.setPointSize(self.browser.width() // 100)
        label.setFont(font)
        for button in self.buttons.values():
            button.setFont(font)
