from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class LevelSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Level:")
        self._add_buttons()

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        available_levels = [1, 2, 3]
        for level in available_levels:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(f"Level {level}")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.initial_selection_widget.on_level_button_clicked(l)
            )
            hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)
