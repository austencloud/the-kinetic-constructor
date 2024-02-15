from enum import Enum


class LetterConditions(Enum):
    PRO = "pro"
    ANTI = "anti"
    DASH = "dash"
    STATIC = "static"
    ALPHA_ENDING = "alpha_ending"
    BETA_ENDING = "beta_ending"
    GAMMA_ENDING = "gamma_ending"
    ALPHA_STARTING = "alpha_starting"
    BETA_STARTING = "beta_starting"
    GAMMA_STARTING = "gamma_starting"
    FOUR_VARIATIONS = "four_variations"
    EIGHT_VARIATIONS = "eight_variations"
    SIXTEEN_VARIATIONS = "sixteen_variations"
    HYBRID = "hybrid"
    NON_HYBRID = "non_hybrid"
    TYPE1_HYBRID = "type1_hybrids"
    TYPE1_NON_HYBRID = "type1_non_hybrids"


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
    def get_letters_by_condition(condition: LetterConditions) -> list:
        """
        Returns a list of letter enums based on a given condition.
        """
        condition_mappings = {
            LetterConditions.PRO: [
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
            LetterConditions.ANTI: [
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
            LetterConditions.DASH: [
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
            LetterConditions.STATIC: [
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
            LetterConditions.ALPHA_ENDING: [
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
            LetterConditions.BETA_ENDING: [
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
            LetterConditions.GAMMA_ENDING: [
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
            LetterConditions.ALPHA_STARTING: [
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
            LetterConditions.BETA_STARTING: [
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
            LetterConditions.GAMMA_STARTING: [
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
            LetterConditions.FOUR_VARIATIONS: [
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
            LetterConditions.EIGHT_VARIATIONS: [
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
            LetterConditions.SIXTEEN_VARIATIONS: [
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
            LetterConditions.HYBRID: [
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
            LetterConditions.NON_HYBRID: [
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
            LetterConditions.TYPE1_HYBRID: [
                Letters.C,
                Letters.F,
                Letters.I,
                Letters.L,
                Letters.O,
                Letters.R,
                Letters.U,
                Letters.V,
            ],
            LetterConditions.TYPE1_NON_HYBRID: [
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
        Convert a string to the corresponding enum member, including handling dashes.
        """
        # Attempt to find a direct match first
        for letter in cls:
            if letter.value == letter_str:
                return letter

        # If no direct match, try to convert dash-containing names
        normalized_str = letter_str.replace("-", "_DASH")
        if normalized_str in cls.__members__:
            return cls.__members__[normalized_str]

        # Raise an error if no match is found
        raise ValueError(f"No matching enum member for string: {letter_str}")

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
