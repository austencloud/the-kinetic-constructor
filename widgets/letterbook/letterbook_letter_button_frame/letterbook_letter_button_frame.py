from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter


from widgets.letterbook.letterbook_letter_button_frame.components.letterbook_letter_button_manager import (
    LetterBookLetterButtonManager,
)


from .components.letterbook_button_frame_styler import LetterBookButtonFrameStyler

if TYPE_CHECKING:
    from widgets.letterbook.letterbook import LetterBook


class LetterBookLetterButtonFrame(QFrame):
    def __init__(self, letterbook: "LetterBook") -> None:
        super().__init__()
        self.letterbook = letterbook
        self.spacing = 5
        self.outer_frames: dict[str, QFrame] = {}
        self.letter_rows = self._define_letter_rows()
        self.layout_styler = LetterBookButtonFrameStyler(self)
        self.button_manager = LetterBookLetterButtonManager(self)
        self.button_manager.create_buttons()
        self._init_letter_buttons_layout()

    def _define_letter_rows(self) -> dict[str, list[list[Letter]]]:
        return {
            LetterType.Type1: [
                ["A", "B", "C"],
                ["D", "E", "F"],
                ["G", "H", "I"],
                ["J", "K", "L"],
                ["M", "N", "O"],
                ["P", "Q", "R"],
                ["S", "T", "U", "V"],
            ],
            LetterType.Type2: [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
            LetterType.Type3: [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
            LetterType.Type4: [["Φ", "Ψ", "Λ"]],
            LetterType.Type5: [["Φ-", "Ψ-", "Λ-"]],
            LetterType.Type6: [["α", "β", "Γ"]],
        }

    def _init_letter_buttons_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        frame_tuples = []
        stretch_factors = {
            LetterType.Type1: 100,
            LetterType.Type2: 32,
            LetterType.Type3: 32,
            LetterType.Type4: 16,
            LetterType.Type5: 19,
            LetterType.Type6: 16,
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

    def resize_letterbook_letter_button_frame(self) -> None:
        self.button_manager.resize_buttons(self.letterbook.main_widget.height() * 0.6)
