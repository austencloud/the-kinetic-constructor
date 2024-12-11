
from typing import TYPE_CHECKING,
from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging

from Enums.letters import LetterType

from main_window.main_widget.learn_widget.codex_widget.placeholder_pictograph import (
    PlaceholderPictograph,
)

from .codex_constants import SECTIONS_PART1, SECTIONS_PART2, TYPE_MAP  # Import constants

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import (
        Codex,
    )
    from base_widgets.base_pictograph.pictograph_view import PictographView

logger = logging.getLogger(__name__)


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections."""

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.letter_views: dict[str, "PictographView"] = {}

    def load_sections(self):
        self.load_section_with_label(SECTIONS_PART1)
        self.load_section_with_label(SECTIONS_PART2)

    def load_section_with_label(self, sections: list[list[list[str]]]):
        """
        Loads a major section of the codex (like PART1 or PART2) and determines
        the letter type from the first letter in this section to display a heading label.
        """
        from base_widgets.base_pictograph.base_pictograph import BasePictograph
        from base_widgets.base_pictograph.pictograph_view import PictographView

        first_letter = sections[0][0][0]  # First letter of the first row
        pictograph_dict = self.codex.pictograph_data.get(first_letter, None)
        if pictograph_dict and "letter_type" in pictograph_dict:
            try:
                letter_type_enum = LetterType[pictograph_dict["letter_type"]]
                type_label_str = f"Type {letter_type_enum.value}: {TYPE_MAP.get(letter_type_enum, 'Unknown Type')}"
            except KeyError:
                type_label_str = "Type Unknown: Unknown Type"
        else:
            type_label_str = "Type Unknown: Unknown Type"

        type_label = QLabel()
        type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font = QFont()
        font.setBold(True)
        type_label.setFont(font)
        type_label.setText(type_label_str)
        self.codex.main_vlayout.addWidget(type_label)

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        row_counter = 0
        for section in sections:
            for row_letters in section:
                col_counter = 0
                for letter_str in row_letters:
                    p_dict = self.codex.pictograph_data.get(letter_str, None)
                    if p_dict:
                        scene = BasePictograph(self.codex.main_widget)
                        scene.updater.update_pictograph(p_dict)

                        view = PictographView(scene)
                        self.letter_views[letter_str] = view
                        grid.addWidget(view, row_counter, col_counter)
                    else:
                        logger.warning(
                            f"Pictograph data for letter '{letter_str}' is incomplete or missing. Using placeholder."
                        )
                        scene = PlaceholderPictograph(self.codex.main_widget)
                        view = PictographView(scene)
                        self.letter_views[letter_str] = view
                        grid.addWidget(view, row_counter, col_counter)
                    col_counter += 1
                row_counter += 1

        self.codex.main_vlayout.addLayout(grid)
