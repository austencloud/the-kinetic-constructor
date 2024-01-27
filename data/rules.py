from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Positions


# Define the letter groups
alpha_ending_letters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "W",
    "X",
    "W-",
    "X-",
    "Φ",
    "Φ-",
    "α",
]
beta_ending_letters = [
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "Y",
    "Z",
    "Y-",
    "Z-",
    "Ψ",
    "Ψ-",
    "β",
]
gamma_ending_letters = [
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "Σ",
    "Δ",
    "θ",
    "Ω",
    "Σ-",
    "Δ-",
    "θ-",
    "Ω-",
    "Λ",
    "Λ-",
    "Γ",
]

# Define the next possible letters for each group
alpha_starting_letters = [
    "A",
    "B",
    "C",
    "J",
    "K",
    "L",
    "Σ",
    "Δ",
    "θ-",
    "Ω-",
    "Ψ",
    "Φ-",
    "α",
]
beta_starting_letters = [
    "G",
    "H",
    "I",
    "D",
    "E",
    "F",
    "Σ-",
    "Δ-",
    "θ",
    "Ω",
    "Φ",
    "Ψ-",
    "β",
]
gamma_starting_letters = [
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "W-",
    "X-",
    "Y-",
    "Z-",
    "Λ",
    "Λ-",
    "Γ",
    "Γ-",
]


def get_next_letters(letter: all_letters) -> list[all_letters]:
    """Return the next possible letters for the given letter."""
    if letter in alpha_ending_letters:
        return alpha_starting_letters
    elif letter in beta_ending_letters:
        return beta_starting_letters
    elif letter in gamma_ending_letters:
        return gamma_starting_letters
    else:
        return []


positions: dict[all_letters, tuple[Positions]] = {
    # Type1
    "A": ("alpha", "alpha"),
    "B": ("alpha", "alpha"),
    "C": ("alpha", "alpha"),
    "D": ("beta", "alpha"),
    "E": ("beta", "alpha"),
    "F": ("beta", "alpha"),
    "G": ("beta", "beta"),
    "H": ("beta", "beta"),
    "I": ("beta", "beta"),
    "J": ("alpha", "beta"),
    "K": ("alpha", "beta"),
    "L": ("alpha", "beta"),
    "M": ("gamma", "gamma"),
    "N": ("gamma", "gamma"),
    "O": ("gamma", "gamma"),
    "P": ("gamma", "gamma"),
    "Q": ("gamma", "gamma"),
    "R": ("gamma", "gamma"),
    "S": ("gamma", "gamma"),
    "T": ("gamma", "gamma"),
    "U": ("gamma", "gamma"),
    "V": ("gamma", "gamma"),
    # Type2
    "W": ("gamma", "alpha"),
    "X": ("gamma", "alpha"),
    "Y": ("gamma", "beta"),
    "Z": ("gamma", "beta"),
    "Σ": ("alpha", "gamma"),
    "Δ": ("alpha", "gamma"),
    "θ": ("beta", "gamma"),
    "Ω": ("beta", "gamma"),
    # Type3
    "W-": ("gamma", "alpha"),
    "X-": ("gamma", "alpha"),
    "Y-": ("gamma", "beta"),
    "Z-": ("gamma", "beta"),
    "Σ-": ("beta", "gamma"),
    "Δ-": ("beta", "gamma"),
    "θ-": ("alpha", "gamma"),
    "Ω-": ("alpha", "gamma"),
    # Type4
    "Φ": ("beta", "alpha"),
    "Ψ": ("alpha", "beta"),
    "Λ": ("gamma", "gamma"),
    # Type5
    "Φ-": ("alpha", "alpha"),
    "Ψ-": ("beta", "beta"),
    "Λ-": ("gamma", "gamma"),
    # Type6
    "α": ("alpha", "alpha"),
    "β": ("beta", "beta"),
    "Γ": ("gamma", "gamma"),
}
