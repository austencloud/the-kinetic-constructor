from typing import TYPE_CHECKING
import logging

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)

from main_window.main_widget.learn_widget.codex.codex_toggle_button import (
    CodexToggleButton,
)

from .codex_control_widget import CodexControlWidget
from .codex_section_manager import CodexSectionManager

from .codex_animation_manager import CodexAnimationManager
from .codex_size_manager import CodexSizeManager

from main_window.main_widget.learn_widget.codex.codex_data_manager import (
    CodexDataManager,
)

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

    def __init__(self, learn_widget: "LearnWidget"):
        """Initializes the Codex with reference to the parent LearnWidget."""
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(0)

        self.section_manager = CodexSectionManager(self)
        self.control_widget = CodexControlWidget(self)
        self.animation_manager = CodexAnimationManager(self)
        self.size_manager = CodexSizeManager(self)
        self.toggle_button = CodexToggleButton(self)

        self._initialize_data()
        self._setup_layout()
        self._setup_scroll_area()
        self._apply_styles()

        self.section_manager.setup_sections()

    def _initialize_data(self) -> None:
        """Initializes Codex data from the CodexDataManager."""
        self.codex_data_manager = CodexDataManager(self.main_widget)
        self.pictograph_data = self.codex_data_manager.get_pictograph_data()

    def _setup_layout(self) -> None:
        """Sets up the main Codex layout with control widget and scroll area."""
        self.main_vlayout = QVBoxLayout(self)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        self.main_vlayout.addWidget(self.control_widget)

    def _setup_scroll_area(self) -> None:
        """Sets up the scroll area and content layout."""
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.main_vlayout.addWidget(self.scroll_area)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.scroll_area.setWidget(content_widget)

        self.lower_hbox = QHBoxLayout()
        self.main_vlayout.addWidget(self.scroll_area)

    def _apply_styles(self) -> None:
        """Applies styling for the Codex and its scroll area."""
        self.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

    def resizeEvent(self, event) -> None:
        """Handles resizing events, adjusting pictograph sizes and spacers."""
        self.size_manager.adjust_pictograph_sizes()
        self.section_manager.spacer_1.changeSize(20, self.height() // 30)
        self.section_manager.spacer_2.changeSize(20, self.height() // 30)
        super().resizeEvent(event)
