from typing import Literal
from enum import Enum


class Letter(Enum):
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
    W_dash = "W-"
    X_dash = "X-"
    Y_dash = "Y-"
    Z_dash = "Z-"
    Sigma = "Σ"
    Delta = "Δ"
    Theta = "θ"
    Omega = "Ω"
    Phi = "Φ"
    Psi = "Ψ"
    Lambda = "Λ"
    Sigma_dash = "Σ-"
    Delta_dash = "Δ-"
    Theta_dash = "θ-"
    Omega_dash = "Ω-"
    Phi_dash = "Φ-"
    Psi_dash = "Ψ-"
    Lambda_dash = "Λ-"
    Alpha = "α"
    Beta = "β"
    Gamma = "Γ"
    Terra = "⊕"
    Tau = "𝛕"
    Mu = "μ"
    Nu = "ν"
    Zeta = "ζ"
    Eta = "η"


Letters = Literal[
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
    "W",
    "X",
    "Y",
    "Z",
    "W-",
    "X-",
    "Y-",
    "Z-",
    "Σ",
    "Δ",
    "θ",
    "Ω",
    "Σ-",
    "Δ-",
    "θ-",
    "Ω-",
    "Φ",
    "Ψ",
    "Λ",
    "Φ-",
    "Ψ-",
    "Λ-",
    "α",
    "β",
    "Γ",
    "⊕",
    "",
    "𝛕",
    "μ",
    "ν",
    "ζ",
    "η",
]

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
