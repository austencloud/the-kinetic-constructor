from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame


class LevelSelector(QWidget):
    def __init__(self, sequence_generator_frame: "BaseSequenceGeneratorFrame"):
        super().__init__()
        self.sequence_generator_frame = sequence_generator_frame
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
        self.sequence_generator_frame._update_sequence_level(level)
        if level == 1:
            self.sequence_generator_frame.turn_intensity_adjuster.hide()
        else:
            self.sequence_generator_frame.turn_intensity_adjuster.show()
            self.sequence_generator_frame.turn_intensity_adjuster.adjust_values(level)

    def set_level(self, level):
        """Set the initial level when loading settings."""
        self._on_level_change(level)

    def resize_level_selector(self):
        font_size = (
            self.sequence_generator_frame.sequence_generator_tab.main_widget.width()
            // 75
        )
        for button in self.level_buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.updateGeometry()
            button.repaint()
        font = self.level_label.font()
        font.setPointSize(font_size)
        self.level_label.setFont(font)
