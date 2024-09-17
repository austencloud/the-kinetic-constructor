from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..base_auto_builder_frame import BaseAutoBuilderFrame


class LevelSelectorWidget(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.level_buttons: dict[str, QPushButton] = {}
        self._create_level_buttons()

    def _create_level_buttons(self):
        levels = [1, 2, 3]  # Level options
        for level in levels:
            button = QPushButton(f"{level}")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, l=level: self._on_level_change(l))
            self.layout.addWidget(button)
            self.level_buttons[f"level_{level}"] = button

    def _on_level_change(self, level):
        for button in self.level_buttons.values():
            button.setChecked(False)
        self.level_buttons[f"level_{level}"].setChecked(True)
        self.auto_builder_frame._update_sequence_level(level)

    def set_level(self, level):
        """Set the initial level when loading settings."""
        self._on_level_change(level)
