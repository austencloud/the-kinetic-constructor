from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtCore import Qt, QSize
from Enums import LetterType
from constants import COLOR, LEAD_STATE, LETTER_BTN_ICON_DIR, MOTION_TYPE
from typing import TYPE_CHECKING, Dict, List, Tuple
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import all_letters
from widgets.filter_tab import FilterTab
from widgets.letter_button_frame.letter_button import LetterButton

if TYPE_CHECKING:
    from widgets.codex.codex_button_panel import CodexButtonPanel
    from widgets.codex.codex import Codex


class LetterButtonClickHandler:
    def __init__(self, letter_button_frame: "LetterButtonFrame"):
        self.lbf = letter_button_frame

    def on_letter_button_clicked(self, letter: str) -> None:
        button = self.lbf.buttons[letter]
        is_selected = letter in self.lbf.button_panel.codex.selected_letters

        if is_selected:
            self.lbf.button_panel.codex.selected_letters.remove(letter)
        else:
            self.lbf.button_panel.codex.selected_letters.append(letter)

        if letter in self.lbf.button_panel.codex.selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            self.lbf.button_panel.codex.scroll_area.section_manager.create_section_if_needed(
                letter_type
            )
        for (
            section
        ) in self.lbf.button_panel.codex.scroll_area.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.filter_tab.show_tabs_based_on_chosen_letters()

        button.setFlat(not is_selected)
        button.setStyleSheet(button.get_button_style(pressed=not is_selected))
        if letter in self.lbf.button_panel.codex.selected_letters:
            self.lbf.process_pictographs_for_letter(letter)
        self.lbf.button_panel.codex.scroll_area.update_pictographs()
        for (
            section
        ) in self.lbf.button_panel.codex.scroll_area.section_manager.sections.values():
            if section.letter_type == LetterType.get_letter_type(letter):
                section.resize_section()
        # After processing selection, update the visibility of sections and tabs
        self.lbf.button_panel.codex.scroll_area.section_manager.update_sections_based_on_letters(
            self.lbf.button_panel.codex.selected_letters
        )


class LetterButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__()
        self.button_panel = button_panel
        self.spacing = 5  # Adjust spacing as needed
        self.buttons: Dict[Letters, LetterButton] = {}
        self.type_frames: Dict[str, QFrame] = {}
        self.letter_rows = self._define_letter_rows()
        self._init_letter_buttons_layout()
        self._connect_letter_buttons()
        self._setup_styles()

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
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)

        # Set the policy to allow the main frame to expand both horizontally and vertically
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        for type_name, rows in self.letter_rows.items():
            border_colors = self.get_border_colors(type_name)
            outer_frame = self.create_styled_frame(border_colors[0], 6)
            outer_frame_layout = QVBoxLayout(outer_frame)
            outer_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            outer_frame.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            if len(border_colors) == 2:
                inner_frame = self.create_styled_frame(border_colors[1], 3, outer_frame)
                inner_frame_layout = QVBoxLayout(inner_frame)
                inner_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
                inner_frame.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                )

                type_frame_layout = inner_frame_layout
            else:
                type_frame_layout = outer_frame_layout

            # Adding stretch to ensure that the layout expands the items within it
            type_frame_layout.addStretch(1)

            for row in rows:
                row_layout = QHBoxLayout()
                row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                row_layout.setSpacing(self.spacing)

                for letter_str in row:
                    button = self._create_letter_button(letter_str)
                    row_layout.addWidget(button)

                # Adding stretch to ensure that the layout expands the items within it
                row_layout.addStretch(1)
                type_frame_layout.addLayout(row_layout)

            # Add stretch to the outer layout to ensure it takes up all available space
            outer_frame_layout.addStretch(1)
            main_layout.addWidget(outer_frame)
            self.type_frames[type_name] = outer_frame

    def get_border_colors(self, type_name: str) -> Tuple[str, str]:
        # Define your border colors based on the type
        border_colors = {
            "Type1": ("#6F2DA8", "#00b3ff"),
            "Type2": ("#6F2DA8", "#6F2DA8"),
            "Type3": ("#6F2DA8", "#26e600"),
            "Type4": ("#26e600", "#26e600"),
            "Type5": ("#00b3ff", "#26e600"),
            "Type6": ("#eb7d00", "#eb7d00"),
        }
        return border_colors[type_name]

    def create_styled_frame(
        self, color: str, border_width: int, parent: QFrame = None
    ) -> QFrame:
        frame = QFrame(parent)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(
            f"border: {border_width}px solid {color}; "
            f"margin: {border_width}px; "
            "background-color: white;"
        )
        return frame

    def _set_frame_borders(self, frame: QFrame, colors):
        if len(colors) == 2:
            # Double border with two colors
            frame.setStyleSheet(
                f"border: 5px solid {colors[0]};"
                f"margin: 5px;"
                f"padding: 5px;"
                f"border-radius: 5px;"
                f"background-color: {colors[1]};"
            )
        else:
            # Single border with one color
            frame.setStyleSheet(
                f"border: 5px solid {colors[0]};" f"border-radius: 5px;"
            )

    def _create_styled_frame(self, color, border_width, parent=None) -> QFrame:
        frame = QFrame(parent)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setStyleSheet(f"border: {border_width}px solid {color};")
        frame.setContentsMargins(0, 0, 0, 0)
        frame.layout().setContentsMargins(0, 0, 0, 0)
        frame.layout().setSpacing(0)
        return frame

    def _create_letter_button(self, letter_str) -> LetterButton:
        letter_type = LetterType.get_letter_type(letter_str)
        icon_path = f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter_str}.svg"
        button = LetterButton(
            icon_path,
            letter_str,
            self.button_panel.codex.main_tab_widget.main_widget,
        )
        self.buttons[letter_str] = button

        # Add horizontal spacing between buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(button)
        button_layout.addSpacing(self.spacing)

        return button

    def get_icon_path(self, letter_type: str, letter: all_letters) -> str:
        return f"{LETTER_BTN_ICON_DIR}/{letter_type}/{letter}.svg"

    def resize_letter_buttons(self) -> None:
        button_row_count = sum(len(rows) for rows in self.letter_rows)
        button_size = int(self.button_panel.codex.height() / (button_row_count + 1))
        icon_size = int(button_size * 0.9)

        for type_frame in self.type_frames.values():
            for row_layout in type_frame.findChildren(QHBoxLayout):
                for i in range(row_layout.count()):
                    button: LetterButton = row_layout.itemAt(i).widget()
                    if button:
                        button.setMinimumSize(QSize(button_size, button_size))
                        button.setMaximumSize(QSize(button_size, button_size))
                        button.setIconSize(QSize(icon_size, icon_size))

    def select_all_letters(self) -> None:
        for button in self.buttons.values():
            button.click()

    def _connect_letter_buttons(self) -> None:
        click_handler = LetterButtonClickHandler(self)
        for letter, button in self.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: click_handler.on_letter_button_clicked(
                    letter
                )
            )

    def process_pictographs_for_letter(self, letter: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        section_manager = self.button_panel.codex.scroll_area.section_manager
        main_widget = self.button_panel.codex.main_tab_widget.main_widget

        section_manager.create_section_if_needed(letter_type)
        section = section_manager.sections[letter_type]
        section.filter_tab.show_tabs_based_on_chosen_letters()
        pictograph_dicts = main_widget.letters.get(letter, [])
        for pictograph_dict in pictograph_dicts:
            self.apply_turns_to_pictograph(pictograph_dict, section.filter_tab)

    def apply_turns_to_pictograph(self, pictograph_dict, filter_tab: FilterTab) -> None:
        p_factory = self.button_panel.codex.scroll_area.pictograph_factory
        pictograph_key = p_factory.generate_pictograph_key_from_dict(pictograph_dict)
        pictograph = p_factory.get_or_create_pictograph(pictograph_key, pictograph_dict)
        filter_tab.apply_turns_to_pictograph(pictograph)
        pictograph.updater.update_pictograph()

    def resize_inner_and_outer_panels_so_that_theyre_large_enough_to_fit_their_contents(
        self,
    ) -> None:
        for type_frame in self.type_frames.values():
            inner_frame = type_frame.findChild(QFrame)
            if inner_frame:
                row_count = inner_frame.layout().count()
                button_height = self.buttons["A"].height()
                inner_frame_height = row_count * button_height
                inner_frame.setFixedHeight(inner_frame_height)
            type_frame_height = inner_frame_height + 12  # Add some extra padding
            type_frame.setFixedHeight(type_frame_height)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize_letter_buttons()
        self.resize_inner_and_outer_panels_so_that_theyre_large_enough_to_fit_their_contents()
        super().resizeEvent(event)
