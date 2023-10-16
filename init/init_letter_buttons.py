#import the necessary things
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QFont
from PyQt5.QtSvg import QSvgRenderer
from settings import GRAPHBOARD_SCALE


class Init_Letter_Buttons():
    def __init__(self, ui_setup, main_window):
        self.init_letter_buttons(ui_setup, main_window)

    def init_letter_buttons(self, ui_setup, main_window):
        letter_buttons_layout = QVBoxLayout()
        letter_buttons_layout.setSpacing(int(10* GRAPHBOARD_SCALE))  # Set the spacing between rows of buttons
        letter_buttons_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top
        letter_rows = [
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I'],
            ['J', 'K', 'L'],
            ['M', 'N', 'O'],
            ['P', 'Q', 'R'],
            ['S', 'T', 'U', 'V'],
            ['W', 'X', 'Y', 'Z'],
            ['Σ', 'Δ', 'θ', 'Ω'],
            # ['Φ', 'Ψ', 'Λ'],
            # ['W-', 'X-', 'Y-', 'Z-'],
            # ['Σ-', 'Δ-', 'θ-', 'Ω-'],
            # ['Φ-', 'Ψ-', 'Λ-'],
            ['α', 'β', 'Γ']
        ]

        for row in letter_rows:
            row_layout = QHBoxLayout()
            for letter in row:
                icon_path = f"images/letters/{letter}.svg"
                renderer = QSvgRenderer(icon_path)

                pixmap = QPixmap(renderer.defaultSize())    
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                button = QPushButton(QIcon(pixmap), "", main_window)
                font = QFont()
                font.setPointSize(int(20*GRAPHBOARD_SCALE))
                button.setFont(font)
                button.setFixedSize(int(65 * GRAPHBOARD_SCALE), int(65 * GRAPHBOARD_SCALE))
                button.clicked.connect(lambda _, l=letter: ui_setup.show_pictograph_selector(l))
                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)

        generate_all_button = QPushButton("Generate All", main_window)
        font = QFont()
        font.setPointSize(int(20 * GRAPHBOARD_SCALE))
        generate_all_button.setFont(font)
        generate_all_button.setFixedSize(int(300*GRAPHBOARD_SCALE), int(80*GRAPHBOARD_SCALE))
        generate_all_button.clicked.connect(lambda: ui_setup.generator.generate_all_pictographs(main_window.staff_manager))
        letter_buttons_layout.addWidget(generate_all_button)
        main_window.upper_layout.addLayout(letter_buttons_layout)