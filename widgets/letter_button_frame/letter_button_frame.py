from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt, QSize
from Enums import LetterType
from constants import COLOR, LEAD_STATE, LETTER_BTN_ICON_DIR, MOTION_TYPE
from typing import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import all_letters
from widgets.letter_button_frame.letter_button import LetterButton

if TYPE_CHECKING:
    from widgets.codex.codex_button_panel import CodexButtonPanel
    from widgets.codex.codex import Codex


class LetterButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__()
        self.button_panel = button_panel
        self.spacing = int(self.width() * 0.01)
        self.buttons: Dict[Letters, LetterButton] = {}
        self.init_letter_buttons_layout()
        self.add_black_borders()
        self.setStyleSheet("QFrame { border: 1px solid black; }")
        self.connect_letter_buttons()

    def add_black_borders(self) -> None:
        for letter in self.buttons:
            button = self.buttons[letter]
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

    def init_letter_buttons_layout(self) -> None:
        letter_buttons_layout = QVBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        letter_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.row_layouts: List[QHBoxLayout] = []

        self.letter_rows = [
            # Type1 - Dual-Shift
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N", "O"],
            ["P", "Q", "R"],
            ["S", "T", "U", "V"],
            # Type2 - Shift
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            # Type3 - Cross-Shift
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            # Type4 - Dash
            ["Φ", "Ψ", "Λ"],
            # Type5 - Dual-Dash
            ["Φ-", "Ψ-", "Λ-"],
            # Type6 - Static
            ["α", "β", "Γ"],
        ]

        for row in self.letter_rows:
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.setSpacing(self.spacing)
            self.row_layouts.append(row_layout)

            for letter_str in row:
                letter_type = LetterType.get_letter_type(letter_str)
                icon_path = self.get_icon_path(letter_type, letter_str)
                button = LetterButton(
                    icon_path,
                    letter_str,
                    self.button_panel.codex.main_tab_widget.main_widget,
                )
                row_layout.addWidget(button)
                self.buttons[
                    letter_str
                ] = button  # Storing the Letters object as the key

            letter_buttons_layout.addLayout(row_layout)

        self.letter_buttons_layout = letter_buttons_layout
        self.setLayout(letter_buttons_layout)

    def get_icon_path(self, letter_type: str, letter: all_letters) -> str:
        return f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter}.svg"

    def resize_letter_buttons(self) -> None:
        self.spacing = int(self.width() * 0.01)
        button_row_count = len(self.letter_rows)
        # button_size = int(
        #     (
        #         self.button_panel.codex.main_tab_widget.main_widget.height()
        #         / button_row_count
        #     )
        #     / 2
        # )
        button_size = int(self.height() / (button_row_count + 1))
        icon_size = int(button_size * 0.9)

        for row_layout in self.row_layouts:
            for i in range(row_layout.count()):
                button: LetterButton = row_layout.itemAt(i).widget()
                if button:
                    button.setMaximumSize(button_size, button_size)
                    button.setIconSize(QSize(icon_size, icon_size))

        self.setMaximumHeight(
            int(self.button_panel.codex.main_tab_widget.main_widget.height() * 0.9)
        )
        available_width = button_size * 4
        self.setMinimumWidth(int(available_width + self.spacing * 3))

    def select_all_letters(self) -> None:
        for button in self.buttons.values():
            button.click()

    def on_letter_button_clicked(self, letter: Letters) -> None:
        button = self.buttons[letter]
        is_selected = letter in self.button_panel.codex.selected_letters

        if is_selected:
            self.button_panel.codex.selected_letters.remove(letter)
        else:
            self.button_panel.codex.selected_letters.append(letter)

        for (
            section
        ) in self.button_panel.codex.scroll_area.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.filter_tab.show_tabs_based_on_chosen_letters()

        button.setFlat(not is_selected)
        button.setStyleSheet(button.get_button_style(pressed=not is_selected))
        if letter in self.button_panel.codex.selected_letters:
            self.process_pictographs_for_letter(letter)
        self.button_panel.codex.scroll_area.update_pictographs()

    def connect_letter_buttons(self) -> None:
        for letter, button in self.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: self.on_letter_button_clicked(letter)
            )

    def process_pictographs_for_letter(self, letter: Letters):
        # Get the current turns values from the attribute panels.
        turns_values = self.button_panel.codex.scroll_area.section_manager.sections[
            LetterType.get_letter_type(letter)
        ].filter_tab.get_current_turns_values()

        # Find the pictographs that this letter can generate.
        pictograph_dicts = (
            self.button_panel.codex.main_tab_widget.main_widget.letters.get(letter, [])
        )

        for pictograph_dict in pictograph_dicts:
            # Generate or retrieve the pictograph instance.
            pictograph_key = self.button_panel.codex.scroll_area.pictograph_factory.generate_pictograph_key_from_dict(
                pictograph_dict
            )
            pictograph = self.button_panel.codex.scroll_area.pictograph_factory.get_or_create_pictograph(
                pictograph_key, pictograph_dict
            )

            # Apply the turns values to the pictograph's motions based on their attributes.
            for motion in pictograph.motions.values():
                motion_type = (
                    motion.motion_type
                )  # Assuming motion has a 'motion_type' attribute
                if motion_type in turns_values[MOTION_TYPE]:
                    motion.turns_manager.set_turns(
                        turns_values[MOTION_TYPE][motion_type]
                    )

                if motion.color in turns_values[COLOR]:
                    motion.turns_manager.set_turns(turns_values[COLOR][motion.color])

                if motion.lead_state in turns_values[LEAD_STATE]:
                    motion.turns_manager.set_turns(
                        turns_values[LEAD_STATE][motion.lead_state]
                    )

            # Update the pictograph to reflect the changes.
            pictograph.updater.update_pictograph()