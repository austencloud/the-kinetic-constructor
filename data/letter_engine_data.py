from settings.string_constants import PRO, ANTI, STATIC

letter_types = {
    "Type 1": [
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
    "Type 2": ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
    "Type 3": ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
    "Type 4": ["Φ", "Ψ", "Λ"],
    "Type 5": ["Φ-", "Ψ-", "Λ-"],
    "Type 6": ["α", "β", "Γ"],
}

motion_type_letter_groups = {
    # Type 1
    "pro_vs_pro": "ADGJMPS",
    "anti_vs_anti": "BEHKNQT",
    "pro_vs_anti": "CFILORUV",
    # Type 2
    "static_vs_pro": "WYΣθ",
    "static_vs_anti": "XZΔΩ",
    # Type 3
    "dash_vs_pro": "W-Y-Σ-θ-",
    "dash_vs_anti": "X-Z-Δ-Ω-",
    # Type 4
    "dash_vs_static": "ΦΨΛ",
    # Type 5
    "dash_vs_dash": "Φ-Ψ-Λ-",
    # Type 6
    "static_vs_static": "αβΓ",
}

motion_type_combinations = {
    (PRO, PRO): "pro_vs_pro",
    (ANTI, ANTI): "anti_vs_anti",
    (STATIC, STATIC): "static_vs_static",
    (PRO, ANTI): "pro_vs_anti",
    (ANTI, PRO): "pro_vs_anti",
    (STATIC, PRO): "static_vs_pro",
    (PRO, STATIC): "static_vs_pro",
    (STATIC, ANTI): "static_vs_anti",
    (ANTI, STATIC): "static_vs_anti",
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
