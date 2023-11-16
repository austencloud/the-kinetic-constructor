# import the necessary things
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QFont, QColor
from PyQt6.QtSvg import QSvgRenderer
from settings.numerical_constants import GRAPHBOARD_SCALE
from data.letter_engine_data import letter_types
from settings.string_constants import LETTER_SVG_DIR
from settings.styles import LETTER_BUTTON_SIZE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from main import MainWindow


class LetterButtonsFrame(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_window: "MainWindow" = main_widget.main_window
        self.letter_buttons_layout = QVBoxLayout()
        self.letter_buttons_layout.setSpacing(int(20 * GRAPHBOARD_SCALE))
        self.letter_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        letter_rows = [
            # Type 1 - Dual-Shift
            ["A", "B", "C"],
            ["D", "E", "F"],
            ["G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N", "O"],
            ["P", "Q", "R"],
            ["S", "T", "U", "V"],
            # Type 2 - Shift
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            # Type 3 - Cross-Shift
            # ['W-', 'X-'],
            # ['Y-', 'Z-'],
            # ['Σ-', 'Δ-'],
            # ['θ-', 'Ω-'],
            # Type 4 - Dash
            # ['Φ', 'Ψ', 'Λ'],
            # Type 5 - Dual-Dash
            # ['Φ-', 'Ψ-', 'Λ-'],
            # Type 6 - Static
            ["α", "β", "Γ"],
        ]

        for row in letter_rows:
            row_layout = QHBoxLayout()
            for letter in row:
                for letter_type in letter_types:
                    if letter in letter_types[letter_type]:
                        break
                icon_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
                renderer = QSvgRenderer(icon_path)

                pixmap = QPixmap(renderer.defaultSize())
                pixmap.fill(QColor(Qt.GlobalColor.white))
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                button = QPushButton(QIcon(pixmap), "", self.main_window)
                font = QFont()
                font.setPointSize(int(20 * GRAPHBOARD_SCALE))
                button.setFont(font)

                button.setFixedSize(LETTER_BUTTON_SIZE)
                row_layout.addWidget(button)
            self.letter_buttons_layout.addLayout(row_layout)
            self.letter_buttons_layout.addStretch(1)

        self.main_window.optionboard_layout.addLayout(self.letter_buttons_layout)
