# codex.py

from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QComboBox, QPushButton
import logging

from .codex_control_widget import CodexControlWidget
from .codex_section_manager import CodexSectionManager
from .codex_modification_manager import CodexModificationManager
from .codex_animation_manager import CodexAnimationManager
from .codex_size_manager import CodexSizeManager

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

    def __init__(
        self, learn_widget: "LearnWidget", pictograph_data: dict[str, Optional[dict]]
    ):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_data = pictograph_data

        # Main vertical layout for the Codex
        self.main_vlayout = QVBoxLayout(self)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        # Create the control widget and add it to the top of the layout
        self.control_widget = CodexControlWidget(self)
        self.main_vlayout.addWidget(self.control_widget)

        # Create and configure the scroll area for content
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.scroll_area.setWidget(content_widget)

        self.main_vlayout.addWidget(self.scroll_area)

        self.section_manager = CodexSectionManager(self)
        self.modification_manager = CodexModificationManager(self)
        self.animation_manager = CodexAnimationManager(self)
        self.size_manager = CodexSizeManager(self)

        # Load sections after everything is set up
        self.section_manager.load_sections()

        # Set the background to transparent
        self.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

    def resizeEvent(self, event):
        logger.debug("CodexWidget resized.")
        self.size_manager.adjust_pictograph_sizes()
        super().resizeEvent(event)

    def toggle_codex(self, show: bool):
        """Toggle the visibility of the codex with animation."""
        self.animation_manager.toggle_codex(show)
