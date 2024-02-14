from typing import list
from Enums.Enums import LetterType


class SectionOrganizer:
    SECTION_ORDER = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]

    def get_correct_index_for_section(
        self, letter_type: LetterType, ordered_section_types: list[str]
    ) -> int:
        try:
            desired_position = self.SECTION_ORDER.index(letter_type)
            current_positions = [
                self.SECTION_ORDER.index(typ) for typ in ordered_section_types
            ]
            insert_before = next(
                (
                    i
                    for i, pos in enumerate(current_positions)
                    if pos > desired_position
                ),
                len(ordered_section_types),
            )
            return insert_before
        except ValueError:
            return len(ordered_section_types)
