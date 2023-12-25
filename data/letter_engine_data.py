from constants.string_constants import ANTI, DASH, PRO, STATIC


motion_type_letter_groups = {
    # Type 1
    "pro_vs_pro": "ADGJMPS",
    "anti_vs_anti": "BEHKNQT",
    "pro_vs_anti": "CFILORUV",
    # Type 2
    "pro_vs_static": "WYΣθ",
    "anti_vs_static": "XZΔΩ",
    # Type 3
    "pro_vs_dash": "W-Y-Σ-θ-",
    "anti_vs_dash": "X-Z-Δ-Ω-",
    # Type 4
    "dash_vs_static": "ΦΨΛ",
    # Type 5
    "dash_vs_dash": "Φ-Ψ-Λ-",
    # Type 6
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
