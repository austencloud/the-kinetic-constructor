from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from main_window.main_widget.learn_widget.codex.codex_color_swap_manager import (
    CodexColorSwapManager,
)
from main_window.main_widget.learn_widget.codex.codex_mirror_manager import (
    CodexMirrorManager,
)
from main_window.main_widget.learn_widget.codex.codex_rotation_manager import (
    CodexRotationManager,
)
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex.codex import Codex


class CodexControlWidget(QWidget):
    """Holds Codex buttons: rotate, mirror, color swap, and the orientation selector."""

    ICON_PATH = "images/icons/sequence_widget_icons"

    def __init__(self, codex: "Codex"):
        super().__init__(codex)
        self.codex = codex
        self.mirror_manager = CodexMirrorManager(self)
        self.color_swap_manager = CodexColorSwapManager(self)
        self.rotation_manager = CodexRotationManager(self)
        self.setup_ui()

    def setup_ui(self):
        self.rotate_btn = self._create_button(
            "rotate.png", self.rotation_manager.rotate_codex
        )
        self.mirror_btn = self._create_button(
            "mirror.png", self.mirror_manager.mirror_codex
        )
        self.color_swap_btn = self._create_button(
            "yinyang1.png",
            self.color_swap_manager.swap_colors_in_codex,
        )
        self.orientation_selector = self._create_selector(
            ["in", "clock", "out", "counter"]
        )

        # Set up the layout
        self.top_layout = QHBoxLayout()
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_layout.setContentsMargins(5, 5, 5, 5)  # Small padding for aesthetics
        self.top_layout.setSpacing(10)
        self.top_layout.addWidget(self.rotate_btn)
        self.top_layout.addWidget(self.mirror_btn)
        self.top_layout.addWidget(self.color_swap_btn)
        self.top_layout.addWidget(self.orientation_selector)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.orientation_selector)

        self.setStyleSheet(
            """
            QWidget {
                background: transparent;
            }
            QPushButton {
                background-color: lightgray;
                border: 1px solid gray;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
            }
            QComboBox {
                background-color: lightgray;
                border: 1px solid gray;
                border-radius: 5px;
            }
        """
        )

    def _create_button(self, icon_name: str, callback) -> QPushButton:
        """Utility function to create a styled button with an icon."""
        button = QPushButton()
        icon_path = get_images_and_data_path(f"{self.ICON_PATH}/{icon_name}")
        button.setIcon(QIcon(icon_path))
        button.setFixedSize(40, 40)  # Standard button size
        button.setIconSize(button.size() * 0.8)  # Adjust icon size relative to button
        button.clicked.connect(callback)
        return button

    def _create_selector(self, options: list[str]) -> QComboBox:
        """Utility function to create a styled QComboBox."""
        selector = QComboBox()
        selector.addItems(options)
        selector.setFixedHeight(40)
        return selector

    def resizeEvent(self, event):
        """Adjust icon sizes dynamically on resize."""
        button_size = int(self.codex.height() * 0.05)
        icon_size = QSize(int(button_size * 0.8), int(button_size * 0.8))
        for button in [self.rotate_btn, self.mirror_btn, self.color_swap_btn]:
            button.setFixedSize(button_size, button_size)
            button.setIconSize(icon_size)
        super().resizeEvent(event)
