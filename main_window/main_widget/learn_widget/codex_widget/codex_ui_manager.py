# codex_ui_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex


class CodexUIManager:
    """Manages the UI components of the CodexWidget."""

    def __init__(self, parent: "Codex"):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Main vertical layout is already set in codex_widget.py
        # Set up the top bar with global modifications
        self.setup_top_bar()

    def setup_top_bar(self):
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        self.parent.main_layout = QVBoxLayout(self.parent)

        # Create buttons
        self.parent.rotate_btn = QPushButton("Rotate")
        self.parent.rotate_btn.setObjectName("rotate_btn")
        self.parent.rotate_btn.setFixedHeight(30)

        self.parent.mirror_btn = QPushButton("Mirror")
        self.parent.mirror_btn.setObjectName("mirror_btn")
        self.parent.mirror_btn.setFixedHeight(30)

        self.parent.color_swap_btn = QPushButton("Color Swap")
        self.parent.color_swap_btn.setObjectName("color_swap_btn")
        self.parent.color_swap_btn.setFixedHeight(30)

        # Create orientation selector
        self.parent.orientation_selector = QComboBox()
        self.parent.orientation_selector.addItems(["in", "out"])  # Example orientations
        self.parent.orientation_selector.setObjectName("orientation_selector")
        self.parent.orientation_selector.setFixedHeight(30)

        # Add widgets to top bar
        top_bar.addWidget(self.parent.rotate_btn)
        top_bar.addWidget(self.parent.mirror_btn)
        top_bar.addWidget(self.parent.color_swap_btn)
        top_bar.addWidget(QLabel("Orientation:"))
        top_bar.addWidget(self.parent.orientation_selector)
        top_bar.addStretch()

        self.parent.main_layout.addLayout(top_bar)
