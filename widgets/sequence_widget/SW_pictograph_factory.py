from typing import TYPE_CHECKING
from Enums.Enums import LetterType


from Enums.letters import Letter
from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    END_POS,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    START_POS,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SW_PictographFactory:
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        self.sequence_widget = sequence_widget
        self.pictograph_cache = sequence_widget.main_widget.pictograph_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> Pictograph:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)
        if pictograph_key in self.pictograph_cache.get(letter, {}):
            cached_pictograph = self.pictograph_cache[letter][pictograph_key]
            cached_pictograph.updater.update_pictograph(pictograph_dict)
            return cached_pictograph

        if pictograph_dict is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_dict)

            if letter not in self.pictograph_cache:
                self.pictograph_cache[letter] = {}
            self.pictograph_cache[letter][pictograph_key] = pictograph
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            return pictograph

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def create_pictograph(self) -> Pictograph:
        pictograph = Pictograph(self.sequence_widget.main_widget)
        return pictograph

    def generate_pictograph_key_from_dict(self, pictograph_dict) -> str:
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
        )
