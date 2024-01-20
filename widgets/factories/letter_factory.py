from Enums import LetterNumberType
from widgets.letter import Letter


class LetterFactory:
    _letter_cache = {}

    @classmethod
    def create_letter(cls, letter_str: str) -> Letter:
        if letter_str not in cls._letter_cache:
            cls._letter_cache[letter_str] = Letter(letter_str)
        return cls._letter_cache[letter_str]

