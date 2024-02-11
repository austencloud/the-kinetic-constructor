from Enums import LetterType
from typing import TYPE_CHECKING

from Enums import LetterType
from widgets.scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)


if TYPE_CHECKING:
    from widgets.letter_button_frame.components.sequence_builder_letter_button_manager import (
        OptionPickerLetterButtonManager,
    )


class OptionPickerLetterButtonClickHandler:
    def __init__(
        self, letter_button_manager: "OptionPickerLetterButtonManager"
    ) -> None:
        self.letter_button_manager = letter_button_manager
        self.letter_button_frame = letter_button_manager.letter_button_frame
        self.sequence_builder = self.letter_button_manager.letter_button_frame.codex

    def on_letter_button_clicked(self, letter: str) -> None:
        pass

    def process_pictographs_for_letter(self, letter: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = (
            self.sequence_builder.option_picker.scroll_area.sections_manager
        )
        main_widget = self.sequence_builder.main_widget
        section = section_manager.sections[letter_type]
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.filter_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, filter_tab: FilterTab) -> None:
        pictograph_factory = self.sequence_builder.option_picker.scroll_area.pictograph_factory
        pictograph_key = pictograph_factory.generate_pictograph_key_from_dict(pictograph_dict)
        pictograph = pictograph_factory.get_or_create_pictograph(pictograph_key, pictograph_dict)
        filter_tab.visibility_handler.apply_turns_from_turns_boxes_to_pictograph(
            pictograph
        )
        pictograph.updater.update_pictograph()
