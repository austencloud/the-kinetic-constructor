from enum import Enum


class Letters(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    Σ = "Σ"
    Δ = "Δ"
    θ = "θ"
    Ω = "Ω"
    W_DASH = "W-"
    X_DASH = "X-"
    Y_DASH = "Y-"
    Z_DASH = "Z-"
    Σ_DASH = "Σ-"
    Δ_DASH = "Δ-"
    θ_DASH = "θ-"
    Ω_DASH = "Ω-"
    Φ = "Φ"
    Ψ = "Ψ"
    Λ = "Λ"
    Φ_DASH = "Φ-"
    Ψ_DASH = "Ψ-"
    Λ_DASH = "Λ-"
    α = "α"
    β = "β"
    Γ = "Γ"

    @staticmethod
    def get_letters_by_condition(condition: str) -> list:
        """
        Returns a list of letter enums based on a given condition.
        """
        condition_mappings = {
            "pro": [
                Letters.A,
                Letters.D,
                Letters.G,
                Letters.J,
                Letters.M,
                Letters.P,
                Letters.S,
                Letters.W,
                Letters.W_DASH,
                Letters.Y,
                Letters.Y_DASH,
                Letters.Σ,
                Letters.Σ_DASH,
                Letters.θ,
                Letters.θ_DASH,
            ],
            "anti": [
                Letters.B,
                Letters.E,
                Letters.H,
                Letters.K,
                Letters.N,
                Letters.Q,
                Letters.T,
                Letters.X,
                Letters.X_DASH,
                Letters.Z,
                Letters.Z_DASH,
                Letters.Δ,
                Letters.Δ_DASH,
                Letters.Ω,
                Letters.Ω_DASH,
            ],
            "dash": [
                Letters.W_DASH,
                Letters.X_DASH,
                Letters.Y_DASH,
                Letters.Z_DASH,
                Letters.Σ_DASH,
                Letters.Δ_DASH,
                Letters.θ_DASH,
                Letters.Ω_DASH,
                Letters.Φ,
                Letters.Ψ,
                Letters.Λ,
                Letters.Φ_DASH,
                Letters.Ψ_DASH,
                Letters.Λ_DASH,
            ],
            "static": [
                Letters.W,
                Letters.X,
                Letters.Y,
                Letters.Z,
                Letters.Σ,
                Letters.Δ,
                Letters.θ,
                Letters.Ω,
                Letters.Φ,
                Letters.Ψ,
                Letters.Λ,
                Letters.α,
                Letters.β,
                Letters.Γ,
            ],
            "alpha_ending": [
                Letters.A,
                Letters.B,
                Letters.C,
                Letters.D,
                Letters.E,
                Letters.F,
                Letters.W,
                Letters.X,
                Letters.W_DASH,
                Letters.X_DASH,
                Letters.Φ,
                Letters.Φ_DASH,
                Letters.α,
            ],
            "beta_ending": [
                Letters.G,
                Letters.H,
                Letters.I,
                Letters.J,
                Letters.K,
                Letters.L,
                Letters.Y,
                Letters.Z,
                Letters.Y_DASH,
                Letters.Z_DASH,
                Letters.Ψ,
                Letters.Ψ_DASH,
                Letters.β,
            ],
            "gamma_ending": [
                Letters.M,
                Letters.N,
                Letters.O,
                Letters.P,
                Letters.Q,
                Letters.R,
                Letters.S,
                Letters.T,
                Letters.U,
                Letters.V,
                Letters.Σ,
                Letters.Δ,
                Letters.θ,
                Letters.Ω,
                Letters.Σ_DASH,
                Letters.Δ_DASH,
                Letters.θ_DASH,
                Letters.Ω_DASH,
                Letters.Λ,
                Letters.Λ_DASH,
                Letters.Γ,
            ],
            "alpha_starting": [
                Letters.A,
                Letters.B,
                Letters.C,
                Letters.J,
                Letters.K,
                Letters.L,
                Letters.Σ,
                Letters.Δ,
                Letters.θ_DASH,
                Letters.Ω_DASH,
                Letters.Ψ,
                Letters.Φ_DASH,
                Letters.α,
            ],
            "beta_starting": [
                Letters.G,
                Letters.H,
                Letters.I,
                Letters.D,
                Letters.E,
                Letters.F,
                Letters.Σ_DASH,
                Letters.Δ_DASH,
                Letters.θ,
                Letters.Ω,
                Letters.Φ,
                Letters.Ψ_DASH,
                Letters.β,
            ],
            "gamma_starting": [
                Letters.M,
                Letters.N,
                Letters.O,
                Letters.P,
                Letters.Q,
                Letters.R,
                Letters.S,
                Letters.T,
                Letters.U,
                Letters.V,
                Letters.W,
                Letters.X,
                Letters.Y,
                Letters.Z,
                Letters.W_DASH,
                Letters.X_DASH,
                Letters.Y_DASH,
                Letters.Z_DASH,
                Letters.Λ,
                Letters.Λ_DASH,
                Letters.Γ,
            ],
            "four_variations": [
                Letters.Φ,
                Letters.Ψ,
                Letters.Λ,
                Letters.Φ_DASH,
                Letters.Ψ_DASH,
                Letters.Λ_DASH,
                Letters.α,
                Letters.β,
                Letters.Γ,
            ],
            "eight_variations": [
                Letters.A,
                Letters.B,
                Letters.D,
                Letters.E,
                Letters.G,
                Letters.H,
                Letters.J,
                Letters.K,
                Letters.M,
                Letters.N,
                Letters.P,
                Letters.Q,
            ],
            "sixteen_variations": [
                Letters.C,
                Letters.F,
                Letters.I,
                Letters.L,
                Letters.O,
                Letters.R,
                Letters.U,
                Letters.V,
                Letters.S,
                Letters.T,
                Letters.W,
                Letters.X,
                Letters.Y,
                Letters.Z,
                Letters.W_DASH,
                Letters.X_DASH,
                Letters.Y_DASH,
                Letters.Z_DASH,
                Letters.Σ,
                Letters.Δ,
                Letters.θ,
                Letters.Ω,
                Letters.Σ_DASH,
                Letters.Δ_DASH,
                Letters.θ_DASH,
                Letters.Ω_DASH,
            ],
            "hybrid": [
                Letters.C,
                Letters.F,
                Letters.I,
                Letters.L,
                Letters.O,
                Letters.R,
                Letters.U,
                Letters.V,
                Letters.W,
                Letters.X,
                Letters.Y,
                Letters.Z,
                Letters.W_DASH,
                Letters.X_DASH,
                Letters.Y_DASH,
                Letters.Z_DASH,
                Letters.Σ,
                Letters.Δ,
                Letters.θ,
                Letters.Ω,
                Letters.Σ_DASH,
                Letters.Δ_DASH,
                Letters.θ_DASH,
                Letters.Ω_DASH,
                Letters.Φ,
                Letters.Ψ,
                Letters.Λ,
            ],
            "non_hybrid": [
                Letters.A,
                Letters.B,
                Letters.D,
                Letters.E,
                Letters.G,
                Letters.H,
                Letters.J,
                Letters.K,
                Letters.M,
                Letters.N,
                Letters.P,
                Letters.Q,
                Letters.S,
                Letters.T,
                Letters.Φ_DASH,
                Letters.Ψ_DASH,
                Letters.Λ_DASH,
                Letters.α,
                Letters.β,
                Letters.Γ,
            ],
            "type1_hybrids": [
                Letters.C,
                Letters.F,
                Letters.I,
                Letters.L,
                Letters.O,
                Letters.R,
                Letters.U,
                Letters.V,
            ],
            "type1_non_hybrids": [
                Letters.A,
                Letters.B,
                Letters.D,
                Letters.E,
                Letters.G,
                Letters.H,
                Letters.J,
                Letters.K,
                Letters.M,
                Letters.N,
                Letters.P,
                Letters.Q,
                Letters.S,
                Letters.T,
            ],
        }
        return condition_mappings.get(condition, [])

    @classmethod
    def from_string(cls, letter_str: str):
        """
        Returns the enum member corresponding to the given string.
        """
        for name, member in cls.__members__.items():
            if member.value == letter_str:
                return member
        # Handle dash letters specifically if not found directly
        if letter_str in ["W-", "X-", "Y-", "Z-", "Φ-", "Ψ-", "Λ-"]:
            return cls[letter_str.replace("-", "_DASH")]
        raise ValueError(f"{letter_str} is not a valid Letters enum member.")

    def get_letter(letter_str: str) -> "Letters":
        return Letters(letter_str)


class LetterType(Enum):
    Type1 = (
        [
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
        ],
        "Type1",
    )
    Type2 = (["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"], "Type2")
    Type3 = (["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"], "Type3")
    Type4 = (["Φ", "Ψ", "Λ"], "Type4")
    Type5 = (["Φ-", "Ψ-", "Λ-"], "Type5")
    Type6 = (["α", "β", "Γ"], "Type6")

    def __init__(self, letters, description):
        self._letters = letters
        self._description = description

    @property
    def letters(self):
        return self._letters

    @property
    def description(self):
        return self._description

    @staticmethod
    def get_letter_type(letter: Letters) -> "LetterType":
        letter_str = letter.value
        for letter_type in LetterType:
            if letter_str in letter_type.letters:
                return letter_type
