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

from main_window.main_widget.learn_widget.codex.codex_ori_selector import (
    CodexOriSelector,
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
    """Displays all pictographs with a control panel to modify them."""

    def __init__(self, learn_widget: "LearnWidget"):
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
        self.data_manager = CodexDataManager(self.main_widget)

        self._setup_scroll_area()
        self._setup_layout()

        self.section_manager.setup_sections()



    def _setup_layout(self) -> None:
        """Sets up the main Codex layout with control widget and scroll area."""
        self.main_layout = QVBoxLayout(self)

        self.main_layout.addWidget(self.control_widget)
        self.main_layout.addWidget(self.scroll_area)

    def _setup_scroll_area(self) -> None:
        """Sets up the scroll area and content layout."""
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent;")

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.scroll_area.setWidget(content_widget)

    def resizeEvent(self, event) -> None:
        """Handles resizing events, adjusting pictograph sizes and spacers."""
        self.size_manager.adjust_pictograph_sizes()
        for spacer in self.section_manager.spacers:
            spacer.changeSize(20, self.height() // 30)
        super().resizeEvent(event)
