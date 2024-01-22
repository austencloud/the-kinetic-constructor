from Enums import LetterType
from typing import TYPE_CHECKING

from Enums import LetterType
from widgets.filter_tab import FilterTab

if TYPE_CHECKING:
    from widgets.letter_button_frame.components.letter_button_manager import (
        LetterButtonManager,
    )


class LetterButtonClickHandler:
    def __init__(self, letter_button_manager: "LetterButtonManager") -> None:
        self.letter_button_frame = letter_button_manager.letter_button_frame
        self.button_panel = self.letter_button_frame.button_panel
        self.section_manager = self.button_panel.codex.scroll_area.section_manager

    def on_letter_button_clicked(self, letter: str) -> None:
        button = self.letter_button_frame.button_manager.buttons[letter]
        is_selected = letter in self.button_panel.codex.selected_letters

        if is_selected:
            self.button_panel.codex.selected_letters.remove(letter)
            button.release()
        else:
            self.button_panel.codex.selected_letters.append(letter)
            button.press()

        if letter in self.button_panel.codex.selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            self.section_manager.create_section_if_needed(letter_type)
        for section in self.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.filter_tab.show_tabs_based_on_chosen_letters()

        button.setFlat(not is_selected)

        if letter in self.button_panel.codex.selected_letters:
            self.process_pictographs_for_letter(letter)
        self.button_panel.codex.scroll_area.updater.update_pictographs()
        for section in self.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.resize_section()
        self.section_manager.update_sections_based_on_letters(
            self.button_panel.codex.selected_letters
        )

    def process_pictographs_for_letter(self, letter: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = self.button_panel.codex.scroll_area.section_manager
        main_widget = self.button_panel.codex.main_tab_widget.main_widget

        section_manager.create_section_if_needed(letter_type)
        section = section_manager.sections[letter_type]
        section.filter_tab.show_tabs_based_on_chosen_letters()
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.filter_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, filter_tab: FilterTab) -> None:
        p_factory = self.button_panel.codex.scroll_area.pictograph_factory
        pictograph_key = p_factory.generate_pictograph_key_from_dict(pictograph_dict)
        pictograph = p_factory.get_or_create_pictograph(pictograph_key, pictograph_dict)
        filter_tab.apply_turns_to_pictograph(pictograph)
        pictograph.updater.update_pictograph()
