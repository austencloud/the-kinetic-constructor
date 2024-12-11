# codex_section_manager.py

from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging

from Enums.letters import LetterType
from main_window.main_widget.learn_widget.codex_widget.codex_pictograph_view import CodexPictographView
from main_window.main_widget.learn_widget.codex_widget.codex_section_type_label import CodexSectionTypeLabel
from main_window.main_widget.learn_widget.codex_widget.placeholder_pictograph import PlaceholderPictograph

# Import your SectionTypeLabel and LetterTypeTextPainter
from .codex_constants import TYPE_MAP  # TYPE_MAP may not be necessary if we get description from letter_type directly

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex
    from base_widgets.base_pictograph.pictograph_view import PictographView

logger = logging.getLogger(__name__)


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections."""

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.letter_views: Dict[str, "PictographView"] = {}

    def load_sections(self):
        """
        Instead of loading hardcoded sections, we iterate over LetterType enums.
        For each LetterType:
        - Add a stylized heading
        - Load all pictographs for the letters in that LetterType
        """
        for letter_type in LetterType:
            self.load_letter_type_section(letter_type)

    def load_letter_type_section(self, letter_type: LetterType):
        """
        Load a section for a given LetterType. This includes:
        - A styled heading using SectionTypeLabel
        - A grid of pictographs for all letters in this LetterType
        """
        # Create a stylized heading
        heading_label = CodexSectionTypeLabel(self.codex, letter_type)
        self.codex.main_vlayout.addWidget(heading_label)

        # Now load the pictographs for all letters in this letter_type
        from base_widgets.base_pictograph.base_pictograph import BasePictograph
        from base_widgets.base_pictograph.pictograph_view import PictographView

        letters = letter_type.letters
        if not letters:
            logger.warning(f"No letters found for letter_type: {letter_type}")
            return

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        row_counter = 0
        col_counter = 0
        letters_per_row = 6  # Arbitrary choice; adjust as needed

        for letter_str in letters:
            p_dict = self.codex.pictograph_data.get(letter_str, None)
            if p_dict:
                scene = BasePictograph(self.codex.main_widget)
                scene.updater.update_pictograph(p_dict)
                view = CodexPictographView(scene, self.codex)
                self.letter_views[letter_str] = view
            else:
                logger.warning(
                    f"Pictograph data for letter '{letter_str}' is incomplete or missing. Using placeholder."
                )
                scene = PlaceholderPictograph(self.codex.main_widget)
                view = CodexPictographView(scene)
                self.letter_views[letter_str] = view
            # add a black border around the pictograph view
            grid.addWidget(view, row_counter, col_counter)

            col_counter += 1
            if col_counter >= letters_per_row:
                col_counter = 0
                row_counter += 1

        self.codex.main_vlayout.addLayout(grid)
