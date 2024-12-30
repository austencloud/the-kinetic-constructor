from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from .filter_section_base import FilterSectionBase
from .author_section import AuthorSection
from .contains_letter_section import ContainsLettersSection
from .filter_choice_widget import FilterChoiceWidget
from .grid_mode_section import GridModeSection
from .level_section import LevelSection
from .sequence_length_section import SequenceLengthSection
from .starting_letter_section import StartingLetterSection
from .starting_position_section import StartingPositionSection

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerFilterSelector(QWidget):
    """Widget for initial filter selections in the dictionary browser."""

    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.browse_tab = sequence_picker.browse_tab
        self.selected_letters: set[str] = set()

        # Initialize sections
        self.filter_choice_widget = FilterChoiceWidget(self)
        self.starting_letter_section = StartingLetterSection(self)
        self.contains_letter_section = ContainsLettersSection(self)
        self.length_section = SequenceLengthSection(self)
        self.level_section = LevelSection(self)
        self.starting_position_section = StartingPositionSection(self)
        self.author_section = AuthorSection(self)
        self.grid_mode_section = GridModeSection(self)

        self.section_map: dict[str, QWidget] = {
            "filter_choice": self.filter_choice_widget,
            "starting_letter": self.starting_letter_section,
            "contains_letters": self.contains_letter_section,
            "sequence_length": self.length_section,
            "level": self.level_section,
            "starting_position": self.starting_position_section,
            "author": self.author_section,
            "grid_mode": self.grid_mode_section,
        }

        # Use QStackedWidget to manage sections
        self.stacked_widget = QStackedWidget()
        self.section_indexes = {}
        for name, widget in self.section_map.items():
            index = self.stacked_widget.addWidget(widget)
            self.section_indexes[name] = index

        self.current_filter_section: str = "filter_choice"

        self._setup_ui()

    def _setup_ui(self):
        """Set up the main layout and add the stacked widget."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def show_section(self, section_name: str):
        """Show the specified section using the stacked widget.

        Args:
            section_name (str): The name of the section to display.
        """
        index = self.section_indexes.get(section_name)
        if index is not None:
            self.stacked_widget.setCurrentIndex(index)
            section = self.section_map.get(section_name)
            if section_name != "filter_choice" and isinstance(
                section, FilterSectionBase
            ):
                resize_method = getattr(section, f"resize_{section_name}_section", None)
                if callable(resize_method):
                    resize_method()
            self.browse_tab.browse_tab_settings.set_current_section(section_name)
            self.current_filter_section = section_name
        else:
            print(f"Section '{section_name}' not found.")

    def show_filter_choice_widget(self):
        """Show the filter choice widget."""
        self.show_section("filter_choice")

    def apply_filter(self, filter_key: str, filter_value):
        self.browse_tab.browse_tab_settings.set_current_section("sequence_picker")
        self.browse_tab.filter_manager.apply_current_filter({filter_key: filter_value})

    # Event Handlers
    def on_starting_letter_button_clicked(self, letter: str):
        self.apply_filter("starting_letter", letter)

    def on_length_button_clicked(self, length: int):
        self.apply_filter("sequence_length", length)

    def on_level_button_clicked(self, level: int):
        self.apply_filter("level", level)

    def on_contains_letter_button_clicked(self, letter: str):
        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
        else:
            self.selected_letters.add(letter)

    def apply_contains_letter_filter(self, letters):
        self.apply_filter("contains_letters", letters)

    def on_position_button_clicked(self, position: str):
        self.apply_filter("starting_position", position)

    def on_author_button_clicked(self, author: str):
        self.apply_filter("author", author)

    def on_grid_mode_button_clicked(self, grid_mode: str):
        self.apply_filter("grid_mode", grid_mode)
