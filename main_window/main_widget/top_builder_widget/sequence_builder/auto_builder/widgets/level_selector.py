from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class LevelSelector(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.level_label = QLabel("Level:")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.level_buttons_layout = QHBoxLayout()
        self.level_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.level_buttons: dict[str, QPushButton] = {}
        self._create_level_buttons()

        self.layout.addWidget(self.level_label)
        self.layout.addLayout(self.level_buttons_layout)

    def _create_level_buttons(self):
        levels = [1, 2, 3]
        for level in levels:
            button = QPushButton(f"{level}")
            button.setCheckable(True)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, l=level: self._on_level_change(l))
            self.level_buttons_layout.addWidget(button)
            self.level_buttons[f"level_{level}"] = button

    def _on_level_change(self, level):
        for button in self.level_buttons.values():
            button.setChecked(False)
        self.level_buttons[f"level_{level}"].setChecked(True)
        self.auto_builder_frame._update_sequence_level(level)
        if level == 1:
            self.auto_builder_frame.turn_intensity_adjuster.hide()
        else:
            self.auto_builder_frame.turn_intensity_adjuster.show()
            self.auto_builder_frame.turn_intensity_adjuster.adjust_values(level)

    def set_level(self, level):
        """Set the initial level when loading settings."""
        self._on_level_change(level)

    def resize_level_selector(self):
        font_size = self.auto_builder_frame.auto_builder.main_widget.width() // 60
        for button in self.level_buttons.values():
            button.setStyleSheet(f"font-size: {font_size}px;")
            button.updateGeometry()
            button.repaint()
