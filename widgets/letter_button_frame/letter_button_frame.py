from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.TypeChecking import Letters
from widgets.letter_button_frame.components.letter_button_manager import (
    LetterButtonManager,
)


from .components.letter_button_frame_layout_styler import LetterButtonFrameLayoutStyler

if TYPE_CHECKING:
    from ..codex.codex_button_panel import CodexButtonPanel


class LetterButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__()
        self.button_panel = button_panel
        self.spacing = 5
        self.outer_frames: Dict[str, QFrame] = {}
        self.letter_rows = self._define_letter_rows()
        self.layout_styler = LetterButtonFrameLayoutStyler(self)
        self.button_manager = LetterButtonManager(self)
        self.button_manager.create_buttons()
        self._init_letter_buttons_layout()

    def _define_letter_rows(self) -> Dict[str, List[List[Letters]]]:
        return {
            "Type1": [
                ["A", "B", "C"],
                ["D", "E", "F"],
                ["G", "H", "I"],
                ["J", "K", "L"],
                ["M", "N", "O"],
                ["P", "Q", "R"],
                ["S", "T", "U", "V"],
            ],
            "Type2": [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
            "Type3": [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
            "Type4": [["Φ", "Ψ", "Λ"]],
            "Type5": [["Φ-", "Ψ-", "Λ-"]],
            "Type6": [["α", "β", "Γ"]],
        }

    def _init_letter_buttons_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        frame_tuples = []
        stretch_factors = {
            "Type1": 100,
            "Type2": 32,
            "Type3": 32,
            "Type4": 16,
            "Type5": 19,
            "Type6": 16,
        }
        for type_name, rows in self.letter_rows.items():
            buttons_row_layouts = [
                self.button_manager.get_buttons_row_layout(row) for row in rows
            ]
            outer_frame, _ = self.layout_styler.create_layout(
                type_name, buttons_row_layouts
            )
            self.outer_frames[type_name] = outer_frame
            stretch_factor = stretch_factors.get(type_name, 1)
            self.layout.addWidget(outer_frame, stretch_factor)

        self.layout_styler.add_frames_to_layout(self.layout, frame_tuples)
        self.button_manager.connect_letter_buttons()

    def resize_letter_button_frame(self) -> None:
        self.button_manager.resize_buttons(self.button_panel.codex.height())
