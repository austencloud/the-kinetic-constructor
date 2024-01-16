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
    "A": (PRO, PRO),
    "B": (ANTI, ANTI),
    "C": (PRO, ANTI),
    "D": (PRO, PRO),
    "E": (ANTI, ANTI),
    "F": (PRO, ANTI),
    "G": (PRO, PRO),
    "H": (ANTI, ANTI),
    "I": (PRO, ANTI),
    "J": (PRO, PRO),
    "K": (ANTI, ANTI),
    "L": (PRO, ANTI),
    "M": (PRO, PRO),
    "N": (ANTI, ANTI),
    "O": (PRO, ANTI),
    "P": (PRO, PRO),
    "Q": (ANTI, ANTI),
    "R": (PRO, ANTI),
    "S": (PRO, PRO),
    "T": (ANTI, ANTI),
    "U": (PRO, ANTI),
    "V": (PRO, ANTI),
    "W": (PRO, STATIC),
    "X": (ANTI, STATIC),
    "Y": (PRO, STATIC),
    "Z": (ANTI, STATIC),
    "Σ": (PRO, STATIC),
    "Δ": (ANTI, STATIC),
    "θ": (PRO, STATIC),
    "Ω": (ANTI, STATIC),
    "W-": (PRO, DASH),
    "X-": (ANTI, DASH),
    "Y-": (PRO, DASH),
    "Z-": (ANTI, DASH),
    "Σ-": (PRO, DASH),
    "Δ-": (ANTI, DASH),
    "θ-": (PRO, DASH),
    "Ω-": (ANTI, DASH),
    "Φ": (DASH, STATIC),
    "Ψ": (DASH, STATIC),
    "Λ": (DASH, STATIC),
    "Φ-": (DASH, DASH),
    "Ψ-": (DASH, DASH),
    "Λ-": (DASH, DASH),
    "α": (STATIC, STATIC),
    "β": (STATIC, STATIC),
    "Γ": (STATIC, STATIC),
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
