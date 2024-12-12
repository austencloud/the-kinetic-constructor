# codex_control_widget.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QLabel

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex

class CodexControlWidget(QWidget):
    """
    Holds codex buttons - rotate, mirror, color swap, 
    and the orientation selector.
    """

    def __init__(self, parent: "Codex"):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Adjust spacing as needed

        self.rotate_btn = QPushButton("Rotate")
        self.rotate_btn.setFixedHeight(30)

        self.mirror_btn = QPushButton("Mirror")
        self.mirror_btn.setFixedHeight(30)

        self.color_swap_btn = QPushButton("Color Swap")
        self.color_swap_btn.setFixedHeight(30)

        self.orientation_selector = QComboBox()
        self.orientation_selector.addItems(["in", "clock", "out", "counter"])
        self.orientation_selector.setFixedHeight(30)

        layout.addWidget(self.rotate_btn)
        layout.addWidget(self.mirror_btn)
        layout.addWidget(self.color_swap_btn)
        layout.addWidget(QLabel("Orientation:"))
        layout.addWidget(self.orientation_selector)
        layout.addStretch()
