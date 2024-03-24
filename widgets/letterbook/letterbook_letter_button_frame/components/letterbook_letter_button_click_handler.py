from Enums.Enums import LetterType

from typing import TYPE_CHECKING

from Enums.Enums import LetterType

from widgets.scroll_area.components.section_manager.section_widget.components.turns_tab.turns_tab import (
    TurnsTab,
)


if TYPE_CHECKING:
    from widgets.letterbook.letterbook_letter_button_frame.components.letterbook_letter_button_manager import (
        LetterBookLetterButtonManager,
    )


class LetterBookLetterButtonClickHandler:
    def __init__(self, letter_button_manager: "LetterBookLetterButtonManager") -> None:
        self.letter_button_manager = letter_button_manager
        self.letter_button_frame = letter_button_manager.letter_button_frame
        self.letterbook = self.letter_button_manager.letter_button_frame.letterbook
        self.section_manager = self.letterbook.scroll_area.sections_manager

    def on_letter_button_clicked(self, letter: str) -> None:
        button = self.letter_button_frame.button_manager.buttons[letter]
        is_selected = letter in self.letterbook.selected_letters
        letter_type = LetterType.get_letter_type(letter)

        if is_selected:
            self.letterbook.selected_letters.remove(letter)
            button.release()
        else:
            self.letterbook.selected_letters.append(letter)
            button.press()

        if letter in self.letterbook.selected_letters:
            self.section_manager.create_section_if_needed(letter_type)

        for section in self.section_manager.sections.values():
            if section.letter_type == letter_type:
                section.turns_tab.visibility_handler.update_visibility_based_on_selected_letters()

        button.setFlat(not is_selected)

        if letter in self.letterbook.selected_letters:
            self.process_pictographs_for_letter(letter)

        self.letterbook.update_pictographs()

        for section in self.section_manager.sections.values():
            if section.letter_type == letter_type:
                section.resize_section()
        self.section_manager.update_sections_based_on_letters(
            self.letterbook.selected_letters
        )

    def process_pictographs_for_letter(self, letter: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = self.letterbook.scroll_area.sections_manager
        main_widget = self.letterbook.main_widget
        section = section_manager.sections[letter_type]
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.turns_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, turns_tab: TurnsTab) -> None:
        pictograph_factory = self.letterbook.scroll_area.pictograph_factory
        pictograph_key = self.letterbook.scroll_area.main_widget.pictograph_key_generator.generate_pictograph_key(
            pictograph_dict
        )
        pictograph = pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict
        )
        turns_tab.visibility_handler.apply_turns_from_turns_boxes_to_pictograph(
            pictograph
        )
        pictograph.updater.update_pictograph()
