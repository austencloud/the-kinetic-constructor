class WordSimplifier:
    @staticmethod
    def simplify_repeated_word(word: str) -> str:
        # Function to check if the word can be constructed by repeating a pattern
        def can_form_by_repeating(s: str, pattern: str) -> bool:
            pattern_len = len(pattern)
            return all(
                s[i : i + pattern_len] == pattern for i in range(0, len(s), pattern_len)
            )

        n = len(word)
        # Try to find the smallest repeating unit
        for i in range(1, n // 2 + 1):
            pattern = word[:i]
            if n % i == 0 and can_form_by_repeating(word, pattern):
                return pattern
        return word
