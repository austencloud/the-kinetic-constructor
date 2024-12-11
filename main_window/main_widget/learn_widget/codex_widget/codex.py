from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QComboBox,
)

from .codex_ui_manager import CodexUIManager
from .codex_section_manager import CodexSectionManager
from .codex_modification_manager import CodexModificationManager
from .codex_animation_manager import CodexAnimationManager
from .codex_size_manager import CodexSizeManager
from .codex_constants import (
    SECTIONS_PART1,
    SECTIONS_PART2,
    TYPE_MAP,
)  # Import constants

import logging

if TYPE_CHECKING:
    from PyQt6.QtCore import QPropertyAnimation
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget

logger = logging.getLogger(__name__)


class Codex(QWidget):
    """Container widget for the Codex, managing pictographs and global modifications."""

    rotate_btn: QPushButton
    mirror_btn: QPushButton
    color_swap_btn: QPushButton
    orientation_selector: QComboBox
    animation: "QPropertyAnimation"
    main_layout: QVBoxLayout

    def __init__(
        self, learn_widget: "LearnWidget", pictograph_data: dict[str, Optional[dict]]
    ):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_data = pictograph_data

        self.ui_manager = CodexUIManager(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.main_vlayout = QVBoxLayout(content_widget)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        self.main_layout.addWidget(scroll)
        scroll.setWidget(content_widget)

        self.section_manager = CodexSectionManager(self)
        self.modification_manager = CodexModificationManager(self)
        self.animation_manager = CodexAnimationManager(self)
        self.size_manager = CodexSizeManager(self)
        self.section_manager.load_sections()

    def resizeEvent(self, event):
        logger.debug("CodexWidget resized.")
        self.size_manager.adjust_pictograph_sizes()
        super().resizeEvent(event)

    def toggle_codex(self, show: bool):
        """Toggle the visibility of the codex with animation."""
        self.animation_manager.toggle_codex(show)
