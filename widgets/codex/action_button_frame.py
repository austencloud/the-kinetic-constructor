from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFrame

if TYPE_CHECKING:
    from widgets.codex.codex_button_panel import CodexButtonPanel


class ActionButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__(button_panel)
        self.bp = button_panel
        self.select_all_button = self._create_button(
            "Select All", self.bp.select_all_letters
        )
        self.deselect_all_button = self._create_button(
            "Deselect All", self.bp.deselect_all_letters
        )
        # self.generate_all_button = self._create_button(
        #     "Generate All Images 🧨",
        #     self.bp.codex.image_generator.generate_all_images
        # )
        # self.generate_selected_button = self._create_button(
        #     "Generate Selected Images",
        #     self.bp.codex.image_generator.generate_selected_images
        # )
        self._setup_layout()

    def _create_button(self, text: str, callback) -> QPushButton:
        button = QPushButton(text, self)
        button.setStyleSheet("font-size: 16px;")
        button.clicked.connect(callback)
        return button

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.select_all_button)
        layout.addWidget(self.deselect_all_button)
