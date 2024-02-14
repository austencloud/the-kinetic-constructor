from Enums.Enums import LetterType

from typing import TYPE_CHECKING

from Enums.Enums import LetterType

from widgets.scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)


if TYPE_CHECKING:
    from widgets.codex.codex_letter_button_frame.components.codex_letter_button_manager import (
        CodexLetterButtonManager,
    )


class CodexLetterButtonClickHandler:
    def __init__(self, letter_button_manager: "CodexLetterButtonManager") -> None:
        self.letter_button_manager = letter_button_manager
        self.letter_button_frame = letter_button_manager.letter_button_frame
        self.codex = self.letter_button_manager.letter_button_frame.codex
        self.section_manager = self.codex.scroll_area.sections_manager

    def on_letter_button_clicked(self, letter: str) -> None:
        button = self.letter_button_frame.button_manager.buttons[letter]
        is_selected = letter in self.codex.selected_letters
        letter_type = LetterType.get_letter_type(letter)

        if is_selected:
            self.codex.selected_letters.remove(letter)
            button.release()
        else:
            self.codex.selected_letters.append(letter)
            button.press()

        if letter in self.codex.selected_letters:
            self.section_manager.create_section_if_needed(letter_type)

        for section in self.section_manager.sections.values():
            if section.letter_type == letter_type:
                section.filter_tab.visibility_handler.update_visibility_based_on_selected_letters()

        button.setFlat(not is_selected)

        if letter in self.codex.selected_letters:
            self.process_pictographs_for_letter(letter)

        self.codex.update_pictographs(letter_type)
        for section in self.section_manager.sections.values():
            if section.letter_type == letter_type:
                section.resize_section()
        self.section_manager.update_sections_based_on_letters(
            self.codex.selected_letters
        )

    def process_pictographs_for_letter(self, letter: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = self.codex.scroll_area.sections_manager
        main_widget = self.codex.main_widget
        section = section_manager.sections[letter_type]
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.filter_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, filter_tab: FilterTab) -> None:
        pictograph_factory = self.codex.scroll_area.pictograph_factory
        pictograph_key = self.codex.scroll_area.main_widget.pictograph_key_generator.generate_pictograph_key(
            pictograph_dict
        )
        pictograph = pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict
        )
        filter_tab.visibility_handler.apply_turns_from_turns_boxes_to_pictograph(
            pictograph
        )
        pictograph.updater.update_pictograph()
