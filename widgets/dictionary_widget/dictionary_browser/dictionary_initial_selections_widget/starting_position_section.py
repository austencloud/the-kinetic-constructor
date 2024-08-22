from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class StartingPositionSection(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.buttons: dict[str, QPushButton] = {}
        self.initial_selection_widget = initial_selection_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.starting_position_label = QLabel("Select by Starting Position:")
        self.starting_position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.starting_position_label)
        layout.addStretch(1)

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
