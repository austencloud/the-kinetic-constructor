from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class FilterSectionBase(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget", label_text: str):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self._setup_ui(label_text)

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        # Create a top bar with the back button on the left
        top_bar_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(self.initial_selection_widget.show_filter_choice_widget)
        top_bar_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        # Add the label centered below the top bar
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)
