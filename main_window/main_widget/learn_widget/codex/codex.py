import logging
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.learn_widget.codex.codex_scroll_area import CodexScrollArea
from .codex_toggle_button import CodexToggleButton
from .codex_control_widget import CodexControlWidget
from .codex_section_manager import CodexSectionManager
from .codex_animation_manager import CodexAnimationManager
from .codex_size_manager import CodexSizeManager
from .codex_data_manager import CodexDataManager

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget

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

        # Managers
        self.section_manager = CodexSectionManager(self)
        self.animation_manager = CodexAnimationManager(self)
        self.size_manager = CodexSizeManager(self)
        self.data_manager = CodexDataManager(self)

        # Components
        self.toggle_button = CodexToggleButton(self)
        self.control_widget = CodexControlWidget(self)
        self.scroll_area = CodexScrollArea(self)

        # Layout
        self._setup_layout()
        self.section_manager.setup_sections()

    def _setup_layout(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.control_widget)
        self.main_layout.addWidget(self.scroll_area)

    def resizeEvent(self, event) -> None:
        self.size_manager.adjust_pictograph_sizes()
        for spacer in self.section_manager.spacers:
            spacer.changeSize(20, self.height() // 30)
        super().resizeEvent(event)
