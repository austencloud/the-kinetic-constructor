# codex_section_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout
import logging
from Enums.letters import LetterType
from .codex_pictograph_view import CodexPictographView
from .codex_section_type_label import CodexSectionTypeLabel
from .placeholder_pictograph import PlaceholderPictograph
from base_widgets.base_pictograph.base_pictograph import BasePictograph

if TYPE_CHECKING:
    from .codex import Codex
    from base_widgets.base_pictograph.pictograph_view import PictographView

logger = logging.getLogger(__name__)


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections."""

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.letter_views: dict[str, "PictographView"] = {}

    def load_sections(self):
        for letter_type in LetterType:
            self.load_letter_type_section(letter_type)

    def load_letter_type_section(self, letter_type: LetterType):
        """Load a section for a given LetterType."""
        heading_label = CodexSectionTypeLabel(self.codex, letter_type)
        self.codex.main_vlayout.addWidget(heading_label)

        letters = letter_type.letters
        if not letters:
            logger.warning(f"No letters found for letter_type: {letter_type}")
            return

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        row_counter = 0
        col_counter = 0
        letters_per_row = 6

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
            grid.addWidget(view, row_counter, col_counter)

            col_counter += 1
            if col_counter >= letters_per_row:
                col_counter = 0
                row_counter += 1

        self.codex.main_vlayout.addLayout(grid)
