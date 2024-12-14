# codex.py

from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)
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
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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

        # Set size policy to allow maximumWidth to be animated
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(0)  # Start hidden

        # Main layout for the entire Codex widget
        self.main_vlayout = QVBoxLayout(self)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        self.control_widget = CodexControlWidget(self)
        self.main_vlayout.addWidget(self.control_widget)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.scroll_area.setWidget(content_widget)
        self.lower_hbox = QHBoxLayout()

        self.main_vlayout.addWidget(self.scroll_area)

        self.section_manager = CodexSectionManager(self)
        self.modification_manager = CodexModificationManager(self)
        self.animation_manager = CodexAnimationManager(self)
        self.size_manager = CodexSizeManager(self)

        self.section_manager.load_sections()

        self.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

    def resizeEvent(self, event):
        logger.debug("CodexWidget resized.")
        self.size_manager.adjust_pictograph_sizes()
        self.section_manager.spacer_1.changeSize(20, self.height() // 30)
        self.section_manager.spacer_2.changeSize(20, self.height() // 30)
        super().resizeEvent(event)

    def toggle_codex(self, show: bool):
        """Toggle the visibility of the codex with animation."""
        self.animation_manager.toggle_codex(show)
