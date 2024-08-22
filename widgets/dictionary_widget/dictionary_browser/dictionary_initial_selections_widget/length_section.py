from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LengthSection(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.buttons: dict[str, QPushButton] = {}
        self.initial_selection_widget = initial_selection_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.length_label = QLabel("Select by Sequence Length:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.length_label)
        layout.addStretch(1)

        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]
        for i in range(0, len(available_lengths), 4):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for length in available_lengths[i : i + 4]:
                button = QPushButton(str(length))
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.buttons[f"length_{length}"] = button
                button.clicked.connect(
                    lambda checked, l=length: self.initial_selection_widget.on_length_button_clicked(
                        l
                    )
                )
                hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)
