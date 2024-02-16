from Enums.Enums import LetterType
from Enums.MotionAttributes import MotionTypes
from Enums.letters import Letters
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
    Letters.A: (PRO, PRO),
    Letters.B: (ANTI, ANTI),
    Letters.C: (PRO, ANTI),
    Letters.D: (PRO, PRO),
    Letters.E: (ANTI, ANTI),
    Letters.F: (PRO, ANTI),
    Letters.G: (PRO, PRO),
    Letters.H: (ANTI, ANTI),
    Letters.I: (PRO, ANTI),
    Letters.J: (PRO, PRO),
    Letters.K: (ANTI, ANTI),
    Letters.L: (PRO, ANTI),
    Letters.M: (PRO, PRO),
    Letters.N: (ANTI, ANTI),
    Letters.O: (PRO, ANTI),
    Letters.P: (PRO, PRO),
    Letters.Q: (ANTI, ANTI),
    Letters.R: (PRO, ANTI),
    Letters.S: (PRO, PRO),
    Letters.T: (ANTI, ANTI),
    Letters.U: (PRO, ANTI),
    Letters.V: (PRO, ANTI),
    Letters.W: (PRO, STATIC),
    Letters.X: (ANTI, STATIC),
    Letters.Y: (PRO, STATIC),
    Letters.Z: (ANTI, STATIC),
    Letters.Σ: (PRO, STATIC),
    Letters.Δ: (ANTI, STATIC),
    Letters.θ: (PRO, STATIC),
    Letters.Ω: (ANTI, STATIC),
    Letters.W_DASH: (PRO, DASH),
    Letters.X_DASH: (ANTI, DASH),
    Letters.Y_DASH: (PRO, DASH),
    Letters.Z_DASH: (ANTI, DASH),
    Letters.Σ_DASH: (PRO, DASH),
    Letters.Δ_DASH: (ANTI, DASH),
    Letters.θ_DASH: (PRO, DASH),
    Letters.Ω_DASH: (ANTI, DASH),
    Letters.Φ: (DASH, STATIC),
    Letters.Ψ: (DASH, STATIC),
    Letters.Λ: (DASH, STATIC),
    Letters.Φ_DASH: (DASH, DASH),
    Letters.Ψ_DASH: (DASH, DASH),
    Letters.Λ_DASH: (DASH, DASH),
    Letters.α: (STATIC, STATIC),
    Letters.β: (STATIC, STATIC),
    Letters.Γ: (STATIC, STATIC),
}




letter_type_motion_type_map: dict[LetterType, list[MotionTypes]] = {
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
