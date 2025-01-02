from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.base_classes.base_sequence_generator_frame import (
        BaseSequenceGeneratorFrame,
    )
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GeneratorTypeButton(QPushButton):
    def __init__(self, text: str, frame: "BaseSequenceGeneratorFrame", key: str):
        super().__init__(text)
        self.frame = frame
        self.tab = frame.generate_tab
        self.key = key
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self.show_frame)

    def update_style(self, active: bool):
        active_style = "background-color: blue; font-weight: bold;"
        inactive_style = "background-color: none; font-weight: normal;"
        style = active_style if active else inactive_style
        self.setStyleSheet(f"{style} padding: 8px;")

    def resizeEvent(self, event: QEvent):
        font = self.font()
        font.setPointSize(self.tab.main_widget.width() // 90)
        self.setFont(font)
        self.setFixedHeight(self.tab.main_widget.height() // 16)
        self.setFixedWidth(self.tab.main_widget.width() // 10)
        super().resizeEvent(event)

    def show_frame(self):
        fade_manager = self.tab.main_widget.fade_manager
        widgets = [
            self.frame.level_selector,
            self.frame.length_adjuster,
            self.frame.turn_intensity_adjuster,
            self.frame.continuous_rotation_toggle,
            self.frame.letter_type_picker,
            self.frame.permutation_type_toggle,
            self.frame.rotation_type_toggle,
        ]
        widgets = [widget for widget in widgets if widget]
        fade_manager.widget_fader.fade_and_update(widgets, self.frame.show, 300)
