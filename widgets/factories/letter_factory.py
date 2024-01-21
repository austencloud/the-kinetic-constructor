from Enums import LetterType
from utilities.TypeChecking.TypeChecking import Letters


class LetterFactory:
    _letter_cache = {}

    @classmethod
    def create_letter(cls, letter_str: str) -> Letters:
        if letter_str not in cls._letter_cache:
            cls._letter_cache[letter_str] = Letters(letter_str)
        return cls._letter_cache[letter_str]
