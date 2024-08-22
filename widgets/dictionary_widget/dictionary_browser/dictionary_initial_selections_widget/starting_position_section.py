from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class StartingPositionSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Starting Position:")
        self._add_buttons()

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        starting_positions = ["alpha", "beta", "gamma"]
        for position in starting_positions:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(position.capitalize())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"position_{position}"] = button
            button.clicked.connect(
                lambda checked, p=position: self.initial_selection_widget.on_position_button_clicked(p)
            )
            hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)
