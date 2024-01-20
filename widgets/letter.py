from Enums import LetterNumberType


class Letter:
    _cache = dict()
    def __init__(self, letter_str: str) -> None:
        if hasattr(self, 'str'):
            return
        self.str = letter_str
        self.type = self.get_letter_type(letter_str)

    def __new__(cls, letter_str):
        if letter_str in cls._cache:
            return cls._cache[letter_str]
        self = super(Letter, cls).__new__(cls)
        cls._cache[letter_str] = self
        return self


    def __eq__(self, other) -> bool:
        if isinstance(other, Letter):
            return self.str == other.str
        return False

    def __hash__(self) -> int:
        return hash(self.str)

    def __repr__(self) -> str:
        return self.str

    def get_letter_type(self, str: str) -> str | None:
        for letter_type in LetterNumberType:
            if str in letter_type.letters:
                return letter_type.name.replace("_", "").lower().capitalize()
        return None
