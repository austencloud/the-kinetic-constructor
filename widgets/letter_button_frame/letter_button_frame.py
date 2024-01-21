from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt, QSize
from Enums import LetterType
from constants import COLOR, LEAD_STATE, LETTER_BTN_ICON_DIR, MOTION_TYPE
from typing import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import all_letters
from widgets.filter_tab import FilterTab
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
        self.type_frames: Dict[str, QFrame] = {}
        self.letter_rows = self._define_letter_rows()
        self._init_letter_buttons_layout()
        self._setup_styles()
        self._connect_letter_buttons()

    def _define_letter_rows(self) -> List[List[Letters]]:
        return [
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
            # Type3 - Cross-Shift
            ["W-", "X-", "Y-", "Z-"],
            # Type4 - Dash
            ["Φ", "Ψ", "Λ"],
            # Type5 - Dual-Dash
            ["Φ-", "Ψ-", "Λ-"],
            # Type6 - Static
            ["α", "β", "Γ"],
        ]

    def _setup_styles(self) -> None:
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

    def _init_letter_buttons_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        self.setContentsMargins(self.spacing, self.spacing, self.spacing, self.spacing)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(self.spacing)

        # Define groups by type for styling
        type_groups = {
            "Type1": self.letter_rows[:4],  # First four rows
            "Type2": self.letter_rows[4:6],  # and so on...
            "Type3": self.letter_rows[6:8],
            "Type4": self.letter_rows[8:9],
            "Type5": self.letter_rows[9:10],
            "Type6": self.letter_rows[10:],
        }

        # Colors corresponding to the type
        border_colors = {
            "Type1": "#00b3ff",
            "Type2": "#6F2DA8",
            "Type3": "#ED1C24",
            "Type4": "#2E3192",
            "Type5": "#FF7F27",
            "Type6": "#00A651",
        }

        for type_name, rows in type_groups.items():
            type_frame = QFrame()
            type_frame_layout = QVBoxLayout(type_frame)
            type_frame.setFrameShape(QFrame.Shape.Box)
            type_frame.setStyleSheet(
                f"border: 3px solid {border_colors[type_name]}; padding: 5px;"
            )
            type_frame_layout.setSpacing(self.spacing)

            for row in rows:
                row_layout = QHBoxLayout()
                row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_layout.setSpacing(self.spacing)

                for letter_str in row:
                    letter_type = LetterType.get_letter_type(letter_str)
                    icon_path = f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter_str}.svg"
                    button = LetterButton(
                        icon_path,
                        letter_str,
                        self.button_panel.codex.main_tab_widget.main_widget,
                    )
                    row_layout.addWidget(button)
                    self.buttons[letter_str] = button

                type_frame_layout.addLayout(row_layout)

            main_layout.addWidget(type_frame)
            self.type_frames[type_name] = type_frame

    def get_icon_path(self, letter_type: str, letter: all_letters) -> str:
        return f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter}.svg"

    def resize_letter_buttons(self) -> None:
        button_row_count = sum(len(rows) for rows in self.letter_rows)
        button_size = int(self.height() / (button_row_count + 1))
        icon_size = int(button_size * 0.9)

        for type_frame in self.type_frames.values():
            for row_layout in type_frame.findChildren(QHBoxLayout):
                for i in range(row_layout.count()):
                    button: LetterButton = row_layout.itemAt(i).widget()
                    if button:
                        button.setMaximumSize(QSize(button_size, button_size))
                        button.setIconSize(QSize(icon_size, icon_size))

        self.setMaximumHeight(
            int(self.button_panel.codex.main_tab_widget.main_widget.height() * 0.9)
        )
        available_width = button_size * 4  # Assuming 4 buttons max per row
        self.setMinimumWidth(
            int(available_width + self.spacing * (button_row_count - 1))
        )

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

        if letter in self.button_panel.codex.selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            self.button_panel.codex.scroll_area.section_manager.create_section_if_needed(
                letter_type
            )
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
        for (
            section
        ) in self.button_panel.codex.scroll_area.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.resize_section()

    def _connect_letter_buttons(self) -> None:
        for letter, button in self.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: self.on_letter_button_clicked(letter)
            )

    def process_pictographs_for_letter(self, letter: Letters) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = self.button_panel.codex.scroll_area.section_manager
        main_widget = self.button_panel.codex.main_tab_widget.main_widget

        section_manager.create_section_if_needed(letter_type)
        section = section_manager.sections[letter_type]
        section.filter_tab.show_tabs_based_on_chosen_letters()
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.filter_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, filter_tab: FilterTab):
        p_factory = self.button_panel.codex.scroll_area.pictograph_factory
        pictograph_key = p_factory.generate_pictograph_key_from_dict(pictograph_dict)
        pictograph = p_factory.get_or_create_pictograph(pictograph_key, pictograph_dict)
        filter_tab.apply_turns_to_pictograph(pictograph)
        pictograph.updater.update_pictograph()
