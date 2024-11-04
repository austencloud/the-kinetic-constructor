from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.auto_builder.sequence_generator_widget import (
        SequenceGeneratorWidget,
    )
    from main_window.main_widget.sequence_builder.auto_builder.base_classes.base_auto_builder_frame import (
        BaseAutoBuilderFrame,
    )


class CustomizeSequenceLabel(QLabel):
    def __init__(self, generator_widget: "SequenceGeneratorWidget") -> None:
        super().__init__(generator_widget)
        self.generator_widget = generator_widget
        self.setText("Customize your sequence:")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_stylesheet()

    def set_stylesheet(self) -> None:
        height = self.generator_widget.height()
        font_size = int(0.04 * height)
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.height() // 2}px;"
            f"  font-size: {font_size}px;"
            f"  font-family: 'Monotype Corsiva';"
            f"}}"
        )

    def resize_customize_sequence_label(self) -> None:
        width = self.generator_widget.main_widget.width() // 4
        height = self.generator_widget.main_widget.height() // 20

        self.setFixedSize(width, height)
        self.set_stylesheet()
