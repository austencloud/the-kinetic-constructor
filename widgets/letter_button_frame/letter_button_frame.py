from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.TypeChecking import Letters
from widgets.letter_button_frame.components.letter_button_manager import (
    LetterButtonManager,
)


from .components.letter_button_click_handler import LetterButtonClickHandler
from .components.letter_button_frame_layout_styler import LetterButtonFrameLayoutStyler

if TYPE_CHECKING:
    from ..codex.codex_button_panel import CodexButtonPanel


class LetterButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__()
        self.button_panel = button_panel
        self.spacing = 5  # Adjust spacing as needed
        self.type_frames: Dict[str, QFrame] = {}

        # Define letter rows before initializing the button manager
        self.letter_rows = self._define_letter_rows()

        # Now we can safely initialize the button manager
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

    def _setup_styles(self) -> None:
        for letter in self.button_manager.buttons:
            button = self.button_manager.buttons[letter]
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 0px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
                QPushButton:pressed {
                    background-color: #cce0ff;
                }
                """
            )
        self.setStyleSheet(
            """
            QFrame {
                border: 1px solid black;
            }
            """
        )

    def _init_letter_buttons_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)

        for type_name, rows in self.letter_rows.items():
            buttons_row_layouts = [
                self.button_manager.get_buttons_row_layout(row) for row in rows
            ]
            outer_frame, outer_frame_layout = self.layout_styler.create_layout(
                type_name, buttons_row_layouts
            )
            self.type_frames[type_name] = outer_frame
            main_layout.addWidget(outer_frame)

        main_layout.addStretch(1)

    def resize_inner_and_outer_panels_so_that_theyre_large_enough_to_fit_their_contents(
        self,
    ) -> None:
        for type_frame in self.type_frames.values():
            inner_frame = type_frame.findChild(QFrame)
            if inner_frame:
                row_count = inner_frame.layout().count()
                button_height = self.button_manager.buttons["A"].height()
                inner_frame_height = row_count * button_height
                inner_frame.setFixedHeight(inner_frame_height)
            type_frame_height = inner_frame_height + 12  # Add some extra padding
            type_frame.setFixedHeight(type_frame_height)

    def resize_letter_button_frame(self) -> None:
        self.button_manager.resize_buttons(self.button_panel.codex.height())
        self.resize_inner_and_outer_panels_so_that_theyre_large_enough_to_fit_their_contents()
