from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.auto_builder.base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class CustomizeSequenceLabel(QLabel):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame") -> None:
        super().__init__(auto_builder_frame)
        self.auto_builder_frame = auto_builder_frame
        self.set_default_text()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_stylesheet()

    def set_default_text(self) -> None:
        self.setText("Customize Your Sequence")

    def set_stylesheet(self) -> None:
        width = self.auto_builder_frame.width()
        font_size = int(0.04 * width)
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.height() // 2}px;"
            f"  font-size: {font_size}px;"
            f"  font-family: 'Monotype Corsiva';"
            f"}}"
        )

    def resize_customize_sequence_label(self) -> None:
        width = self.auto_builder_frame.sequence_generator_tab.width() // 3
        height = self.auto_builder_frame.sequence_generator_tab.height() // 15

        self.setFixedSize(width, height)
        self.set_stylesheet()
