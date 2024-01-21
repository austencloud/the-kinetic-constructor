from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFrame

if TYPE_CHECKING:
    from widgets.codex.codex_button_panel import CodexButtonPanel


class ActionButtonFrame(QFrame):
    def __init__(self, button_panel: "CodexButtonPanel") -> None:
        super().__init__(button_panel)
        self.button_panel = button_panel
        self.buttons = self._setup_action_buttons()
        self._setup_layout()

    def _setup_action_buttons(self) -> Dict[str, QPushButton]:
        buttons = {}
        select_all_button = QPushButton("Select All", self)
        select_all_button.setStyleSheet("font-size: 16px;")
        generate_all_images_button = QPushButton("Generate All Images 🧨", self)
        generate_all_images_button.setStyleSheet("font-size: 16px;")
        generate_selected_images_button = QPushButton("Generate Selected Images", self)
        generate_selected_images_button.setStyleSheet("font-size: 16px;")
        select_all_button.clicked.connect(self.button_panel.select_all_letters)
        generate_all_images_button.clicked.connect(
            self.button_panel.codex.image_generator.generate_all_images
        )
        generate_selected_images_button.clicked.connect(
            self.button_panel.codex.image_generator.generate_selected_images
        )
        buttons["select_all_button"] = select_all_button
        buttons["generate_all_button"] = generate_all_images_button
        buttons["generate_selected_button"] = generate_selected_images_button
        return buttons

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for button in self.buttons.values():
            layout.addWidget(button)
