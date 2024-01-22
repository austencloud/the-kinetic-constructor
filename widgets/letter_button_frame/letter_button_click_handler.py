from Enums import LetterType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.letter_button_frame.letter_button_frame import LetterButtonFrame


class LetterButtonClickHandler:
    def __init__(self, letter_button_frame: "LetterButtonFrame"):
        self.lbf = letter_button_frame
        self.button_panel = self.lbf.button_panel
        self.section_manager = self.button_panel.codex.scroll_area.section_manager

    def on_letter_button_clicked(self, letter: str) -> None:
        button = self.lbf.buttons[letter]
        is_selected = letter in self.button_panel.codex.selected_letters

        if is_selected:
            self.button_panel.codex.selected_letters.remove(letter)
        else:
            self.button_panel.codex.selected_letters.append(letter)

        if letter in self.button_panel.codex.selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            self.section_manager.create_section_if_needed(letter_type)
        for section in self.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.filter_tab.show_tabs_based_on_chosen_letters()

        button.setFlat(not is_selected)
        button.setStyleSheet(button.get_button_style(pressed=not is_selected))
        if letter in self.button_panel.codex.selected_letters:
            self.lbf.process_pictographs_for_letter(letter)
        self.button_panel.codex.scroll_area.update_pictographs()
        for section in self.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.resize_section()
        self.section_manager.update_sections_based_on_letters(
            self.button_panel.codex.selected_letters
        )
