from typing import dict, list
from Enums.Enums import LetterType

from Enums.Enums import LetterType
from widgets.pictograph.pictograph import Pictograph


class PictographOrganizer:
    def __init__(self):
        self.pictographs_by_type: dict[LetterType, list[Pictograph]] = {}

    def organize_pictographs_by_type(self, pictographs: dict[str, Pictograph]):
        for key, pictograph in pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            if letter_type not in self.pictographs_by_type:
                self.pictographs_by_type[letter_type] = []
            self.pictographs_by_type[letter_type].append(pictograph)

    def get_pictograph_letter_type(self, pictograph_key: str) -> LetterType:
        letter = pictograph_key.split("_")[0]
        return LetterType.get_letter_type(letter)
