# import the necessary things
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QSize
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
        self.width = int(self.main_window.width() * 0.15)
        self.setMaximumWidth(
            int(self.main_window.width() * 0.15)
        )  # set maximum width to 20% of window width

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
            # ["W-", "X-", "Y-", "Z-"],
            # ["Σ-", "Δ-", "θ-", "Ω-"],
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
                font.setPointSize(int(20))
                button.setFont(font)

                # Set the fixed size of the button
                button_size = int(self.main_window.width() * 0.025)
                button.setFixedSize(button_size, button_size)

                # Set icon size (slightly smaller than button for best appearance)
                icon_size = int(button_size * 0.8)  # 80% of the button size
                button.setIconSize(QSize(int(button.width() * 0.8), int(button.height() * 0.8)))

                row_layout.addWidget(button)
            self.letter_buttons_layout.addLayout(row_layout)
            self.letter_buttons_layout.addStretch(1)

        self.setLayout(self.letter_buttons_layout)
        self.main_window.optionboard_layout.addWidget(self)


# write me a python script that iterates over all the svgs in a given folder and makes them 120x120, leaving the current contents centered by adding the space on the edges equally.
