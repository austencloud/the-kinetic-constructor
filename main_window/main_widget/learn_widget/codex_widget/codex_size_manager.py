# codex_size_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize
import logging

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex

logger = logging.getLogger(__name__)


class CodexSizeManager:
    """Manages dynamic resizing of pictographs within the CodexWidget."""

    def __init__(self, parent: "Codex"):
        self.parent = parent

    def adjust_pictograph_sizes(self):
        codex_width = (
            self.parent.width()
            - self.parent.main_vlayout.contentsMargins().left()
            - self.parent.main_vlayout.contentsMargins().right()
        )
        square_size = codex_width // 6  # Adjusted to divide by 6 as per requirement
        logger.debug(f"Adjusting pictograph sizes to {square_size}x{square_size}.")

        for view in self.parent.section_manager.pictograph_views.values():
            view.setFixedSize(QSize(square_size, square_size))
