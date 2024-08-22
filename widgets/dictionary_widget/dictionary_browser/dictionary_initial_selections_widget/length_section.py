from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class LengthSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Sequence Length:")
        self._add_buttons()

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]
        for i in range(0, len(available_lengths), 4):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for length in available_lengths[i : i + 4]:
                button = QPushButton(str(length))
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.buttons[f"length_{length}"] = button
                button.clicked.connect(
                    lambda checked, l=length: self.initial_selection_widget.on_length_button_clicked(l)
                )
                hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)
