from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)
import logging
from Enums.letters import LetterType
from .codex_pictograph_view import CodexPictographView
from .codex_section_type_label import CodexSectionTypeLabel
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .codex import Codex
    from base_widgets.base_pictograph.pictograph_view import PictographView

logger = logging.getLogger(__name__)


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections."""

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.pictograph_views: dict[str, "PictographView"] = {}
        self.custom_rows = [
            ["A", "B", "C", "D", "E", "F"],
            ["G", "H", "I", "J", "K", "L"],
            ["M", "N", "O", "P", "Q", "R"],
            ["S", "T", "U", "V"],
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            ["Φ", "Ψ", "Λ"],
            ["Φ-", "Ψ-", "Λ-"],
            ["α", "β", "Γ"],
        ]

    def load_sections(self):
        for letter_type in LetterType:
            self.load_letter_type_section(letter_type)

    def load_letter_type_section(self, letter_type: LetterType):
        """Load a section for a given LetterType."""
        heading_label = CodexSectionTypeLabel(self.codex, letter_type)
        self.spacer_1 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.spacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.codex.content_layout.addSpacerItem(self.spacer_1)
        self.codex.content_layout.addWidget(
            heading_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.codex.content_layout.addSpacerItem(self.spacer_2)
        logger.debug("Added extra spacer below the heading label.")

        letters = letter_type.letters
        if not letters:
            logger.warning(f"No letters found for letter_type: {letter_type}")
            return

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(0)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        for row_index, row_letters in enumerate(self.custom_rows):
            current_letters = [letter for letter in row_letters if letter in letters]
            if not current_letters:
                continue

            horizontal_layout = QHBoxLayout()
            horizontal_layout.setSpacing(0)
            horizontal_layout.setContentsMargins(0, 0, 0, 0)

            needs_centering = len(current_letters) == 4 or len(current_letters) == 3

            has_six_pictographs = len(current_letters) == 6 and row_index < 3

            if has_six_pictographs:
                outer_left_spacer = QSpacerItem(
                    20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
                )
                horizontal_layout.addSpacerItem(outer_left_spacer)
                logger.debug(f"Added outer left spacer for row {row_index + 1}.")

            left_spacer = QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            horizontal_layout.addSpacerItem(left_spacer)
            logger.debug(f"Added left spacer for centering row {row_index + 1}.")

            for letter_str in current_letters:
                p_dict = self.codex.pictograph_data.get(letter_str, None)
                if p_dict:
                    if letter_str not in self.pictograph_views:
                        scene = BasePictograph(self.codex.main_widget)
                        view = CodexPictographView(scene, self.codex)
                        scene.updater.update_pictograph(p_dict)
                        self.pictograph_views[letter_str] = view
                        logger.debug(
                            f"Created new CodexPictographView for letter '{letter_str}'"
                        )
                    else:
                        view = self.pictograph_views[letter_str]
                        logger.debug(
                            f"Reusing existing CodexPictographView for letter '{letter_str}'"
                        )

                    horizontal_layout.addWidget(view)
                else:
                    logger.warning(f"Pictograph data missing for letter '{letter_str}'")

            if has_six_pictographs:
                outer_right_spacer = QSpacerItem(
                    20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
                )
                horizontal_layout.addSpacerItem(outer_right_spacer)
                logger.debug(f"Added outer right spacer for row {row_index + 1}.")

            right_spacer = QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
            horizontal_layout.addSpacerItem(right_spacer)
            logger.debug(f"Added right spacer for centering row {row_index + 1}.")

            vertical_layout.addLayout(horizontal_layout)
            logger.debug(f"Added horizontal layout and line for row {row_index + 1}.")

        self.codex.content_layout.addLayout(vertical_layout)
        logger.debug("Added vertical layout with all rows to the content layout.")

    def reload_sections(self):
        """Reload all sections to reflect updated data."""
        for letter, view in self.pictograph_views.items():
            if letter in self.codex.pictograph_data:
                pictograph_dict = self.codex.pictograph_data[letter]
                view.pictograph.updater.update_pictograph(pictograph_dict)
                view.scene().update()
        logger.debug("Reloaded all sections in Codex.")
