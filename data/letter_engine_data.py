from Enums.Enums import LetterType
from Enums.MotionAttributes import MotionType
from Enums.letters import Letter
from constants import ANTI, DASH, PRO, STATIC


motion_type_letter_groups = {
    # Type1
    "pro_vs_pro": "ADGJMPS",
    "anti_vs_anti": "BEHKNQT",
    "pro_vs_anti": "CFILORUV",
    # Type2
    "pro_vs_static": "WYΣθ",
    "anti_vs_static": "XZΔΩ",
    # Type3
    "pro_vs_dash": "W-Y-Σ-θ-",
    "anti_vs_dash": "X-Z-Δ-Ω-",
    # Type4
    "dash_vs_static": "ΦΨΛ",
    # Type5
    "dash_vs_dash": "Φ-Ψ-Λ-",
    # Type6
    "static_vs_static": "αβΓ",
}

letter_type_to_letter_map = {
    "Type1": "ADGJMPSBEHKNQTCFILORUV",
    "Type2": "WYΣθXZΔΩ",
    "Type3": ["W-", "Y-", "Σ-", "θ-", "X-", "Z-", "Δ-", "Ω-"],
    "Type4": "ΦΨΛ",
    "Type5": ["Φ-", "Ψ-", "Λ-"],
    "Type6": "αβΓ",
}

motion_type_combinations = {
    (PRO, PRO): "pro_vs_pro",
    (PRO, ANTI): "pro_vs_anti",
    (PRO, STATIC): "pro_vs_static",
    (PRO, DASH): "pro_vs_dash",
    (ANTI, PRO): "pro_vs_anti",
    (ANTI, ANTI): "anti_vs_anti",
    (ANTI, STATIC): "anti_vs_static",
    (ANTI, DASH): "anti_vs_dash",
    (DASH, PRO): "pro_vs_dash",
    (DASH, ANTI): "anti_vs_dash",
    (DASH, DASH): "dash_vs_dash",
    (DASH, STATIC): "dash_vs_static",
    (STATIC, PRO): "pro_vs_static",
    (STATIC, ANTI): "anti_vs_static",
    (STATIC, DASH): "dash_vs_static",
    (STATIC, STATIC): "static_vs_static",
}

motion_type_letter_combinations = {
    Letter.A: (PRO, PRO),
    Letter.B: (ANTI, ANTI),
    Letter.C: (PRO, ANTI),
    Letter.D: (PRO, PRO),
    Letter.E: (ANTI, ANTI),
    Letter.F: (PRO, ANTI),
    Letter.G: (PRO, PRO),
    Letter.H: (ANTI, ANTI),
    Letter.I: (PRO, ANTI),
    Letter.J: (PRO, PRO),
    Letter.K: (ANTI, ANTI),
    Letter.L: (PRO, ANTI),
    Letter.M: (PRO, PRO),
    Letter.N: (ANTI, ANTI),
    Letter.O: (PRO, ANTI),
    Letter.P: (PRO, PRO),
    Letter.Q: (ANTI, ANTI),
    Letter.R: (PRO, ANTI),
    Letter.S: (PRO, PRO),
    Letter.T: (ANTI, ANTI),
    Letter.U: (PRO, ANTI),
    Letter.V: (PRO, ANTI),
    Letter.W: (PRO, STATIC),
    Letter.X: (ANTI, STATIC),
    Letter.Y: (PRO, STATIC),
    Letter.Z: (ANTI, STATIC),
    Letter.Σ: (PRO, STATIC),
    Letter.Δ: (ANTI, STATIC),
    Letter.θ: (PRO, STATIC),
    Letter.Ω: (ANTI, STATIC),
    Letter.W_DASH: (PRO, DASH),
    Letter.X_DASH: (ANTI, DASH),
    Letter.Y_DASH: (PRO, DASH),
    Letter.Z_DASH: (ANTI, DASH),
    Letter.Σ_DASH: (PRO, DASH),
    Letter.Δ_DASH: (ANTI, DASH),
    Letter.θ_DASH: (PRO, DASH),
    Letter.Ω_DASH: (ANTI, DASH),
    Letter.Φ: (DASH, STATIC),
    Letter.Ψ: (DASH, STATIC),
    Letter.Λ: (DASH, STATIC),
    Letter.Φ_DASH: (DASH, DASH),
    Letter.Ψ_DASH: (DASH, DASH),
    Letter.Λ_DASH: (DASH, DASH),
    Letter.α: (STATIC, STATIC),
    Letter.β: (STATIC, STATIC),
    Letter.Γ: (STATIC, STATIC),
}


letter_type_motion_type_map: dict[LetterType, list[MotionType]] = {
    "Type1": [PRO, ANTI],
    "Type2": [PRO, ANTI, STATIC],
    "Type3": [PRO, ANTI, DASH],
    "Type4": [DASH, STATIC],
    "Type5": [DASH, DASH],
    "Type6": [STATIC, STATIC],
}

# Used for differentiating between antiparallel and parallel - Letters, MNOPQR
parallel_combinations = {
    ("n", "e", "w", "s"),
    ("e", "s", "n", "w"),
    ("s", "w", "e", "n"),
    ("w", "n", "s", "e"),
    ("n", "w", "e", "s"),
    ("w", "s", "n", "e"),
    ("s", "e", "w", "n"),
    ("e", "n", "s", "w"),
}
