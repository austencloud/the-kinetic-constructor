from Enums import MotionType
from constants.string_constants import ANTI, DASH, PRO, STATIC


motion_type_letter_groups = {
    # Type 1
    "pro_vs_pro": "ADGJMPS",
    "anti_vs_anti": "BEHKNQT",
    "pro_vs_anti": "CFILORUV",
    # Type 2
    "static_vs_pro": "WYΣθ",
    "static_vs_static": "XZΔΩ",
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
    (PRO, ANTI): "pro_vs_anti",
    
    (STATIC, STATIC): "static_vs_static",
    (STATIC, PRO): "static_vs_pro",
    (STATIC, ANTI): "static_vs_anti",
    
    (DASH, PRO): "dash_vs_pro",
    (DASH, ANTI): "dash_vs_anti",
    (DASH, STATIC): "dash_vs_static",
    (DASH, DASH): "dash_vs_dash",
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
