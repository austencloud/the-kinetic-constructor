# generator_type_toggle.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from pytoggle import PyToggle

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GeneratorTypeToggle(QWidget):
    """
    A toggle for switching between "Freeform" and "Circular".
    If `PyToggle.isChecked()` is False => Freeform
    If `PyToggle.isChecked()` is True  => Circular
    """

    toggled = pyqtSignal(str)

    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(generate_tab)
        self.generate_tab = generate_tab

        # Main layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Labels on either side of the toggle
        self.freeform_label = QLabel("Freeform")
        self.circular_label = QLabel("Circular")

        # The toggle itself
        self.toggle = PyToggle()
        self.toggle.stateChanged.connect(self._toggle_changed)

        # Add widgets to the layout
        self.layout.addWidget(self.freeform_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.circular_label)

        # Initial style
        self.update_label_styles()

    def current_mode(self) -> str:
        return "circular" if self.toggle.isChecked() else "freeform"

    def _toggle_changed(self, state: bool):
        new_mode = "circular" if state else "freeform"
        self.generate_tab.controller.on_mode_changed(new_mode)
        self.update_label_styles()
        self.toggled.emit(new_mode)

    def set_state(self, generator_type: str):
        self.toggle.setChecked(generator_type == "circular")
        self.update_label_styles()

    def update_label_styles(self):
        if self.toggle.isChecked():
            # Circular
            self.freeform_label.setStyleSheet("font-weight: normal; color: gray;")
            self.circular_label.setStyleSheet("font-weight: bold; color: white;")
        else:
            # Freeform
            self.freeform_label.setStyleSheet("font-weight: bold; color: white;")
            self.circular_label.setStyleSheet("font-weight: normal; color: gray;")

    def resizeEvent(self, event):
        font_size = self.generate_tab.main_widget.width() // 75
        font = self.freeform_label.font()
        font.setPointSize(font_size)

        self.freeform_label.setFont(font)
        self.circular_label.setFont(font)

        self.freeform_label.repaint()
        self.circular_label.repaint()
        super().resizeEvent(event)
