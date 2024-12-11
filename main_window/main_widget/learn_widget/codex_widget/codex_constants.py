# codex_constants.py

from Enums.letters import LetterType

# Define the sections for the Codex
SECTIONS_PART1 = [
    [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
    ],
    [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
]

SECTIONS_PART2 = [
    [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
    [["Φ", "Ψ", "Λ"]],
    [["Φ-", "Ψ-", "Λ-"]],
    [["α", "β", "Γ"]],
]

TYPE_MAP = {
    LetterType.Type1: "Dual-Shift",
    LetterType.Type2: "Shift",
    LetterType.Type3: "Cross-Shift",
    LetterType.Type4: "Dash",
    LetterType.Type5: "Dual-Dash",
    LetterType.Type6: "Static",
}
