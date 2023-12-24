from typing import Literal
from enum import Enum



Type1Letters = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
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
]

Type2Letters = Literal[
    "W",
    "X",
    "Y",
    "Z",
    "Σ",
    "Δ",
    "θ",
    "Ω",
]

Type3Letters = Literal[
    "W-",
    "X-",
    "Y-",
    "Z-",
    "Σ-",
    "Δ-",
    "θ-",
    "Ω-",
]

Type4Letters = Literal[
    "Φ",
    "Ψ",
    "Λ",
]

Type5Letters = Literal[
    "Φ-",
    "Ψ-",
    "Λ-",
]

Type6Letters = Literal[
    "α",
    "β",
    "Γ",
]

AlphaEndingLetters = Literal["A", "B", "C", "D", "E", "F", "W", "X", "Φ", "Φ-", "α"]
BetaEndingLetters = Literal["G", "H", "I", "J", "K", "L", "Y", "Z", "Ψ", "Ψ-", "β"]
GammaEndingLetters = Literal[
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
    "Σ-",
    "Δ",
    "Δ-",
    "θ",
    "θ-",
    "Ω",
    "Ω-",
    "Λ",
    "Λ-",
    "Γ",
]

AlphaStartingLetters = Literal[
    "A", "B", "C", "J", "K", "L", "Σ", "Δ", "θ-", "Ω-", "Ψ", "Φ-", "α"
]
BetaStartingLetters = Literal[
    "G", "H", "I", "D", "E", "F", "θ", "Ω", "Σ-", "Δ-", "Ψ-", "Φ", "β"
]
GammaStartingLetters = Literal[
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
]
