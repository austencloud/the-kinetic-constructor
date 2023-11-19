from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtSvg import QSvgRenderer
from data.letter_engine_data import letter_types
from settings.string_constants import LETTER_SVG_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.option_picker.option_picker import OptionPicker
class LetterButtons(QFrame):
    """
    A class representing a frame containing letter buttons.

    Args:
        main_window (MainWindow): The main window object.

    Attributes:
        main_window (MainWindow): The main window object.
        letter_buttons_layout (QVBoxLayout): The layout for the letter buttons.

    Methods:
        __init__(self, main_window: MainWindow): Initializes the LetterButtons object.
        init_letter_buttons_layout(self) -> None: Initializes the layout for the letter buttons.
        get_letter_type(self, letter: str) -> str: Returns the type of the given letter.
        get_icon_path(self, letter_type: str, letter: str) -> str: Returns the icon path for the given letter type and letter.
        create_button(self, icon_path: str) -> QPushButton: Creates a button with the given icon path.
        update_letter_buttons_size(self) -> None: Updates the size of the letter buttons.
    """

    def __init__(self, main_window: "MainWindow", option_picker: "OptionPicker"):
        super().__init__()
        self.main_window = main_window
        self.option_picker = option_picker
        self.init_letter_buttons_layout()

    def init_letter_buttons_layout(self) -> None:
        """
        Initializes the layout for the letter buttons.
        """
        letter_buttons_layout = QVBoxLayout()
        letter_buttons_layout.setSpacing(int(0))
        self.setContentsMargins(0, 0, 0, 0)
        letter_buttons_layout.setContentsMargins(0, 0, 0, 0)
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
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            # Type 4 - Dash
            ['Φ', 'Ψ', 'Λ'],
            # Type 5 - Dual-Dash
            ['Φ-', 'Ψ-', 'Λ-'],
            # Type 6 - Static
            ["α", "β", "Γ"],
        ]

        for row in letter_rows:
            row_layout = QHBoxLayout()

            for letter in row:
                letter_type = self.get_letter_type(letter)
                icon_path = self.get_icon_path(letter_type, letter)
                button = self.create_button(icon_path)
                row_layout.addWidget(button)

            letter_buttons_layout.addLayout(row_layout)

        self.letter_buttons_layout = letter_buttons_layout
        self.setLayout(letter_buttons_layout)
        
    def get_letter_type(self, letter: str) -> str:
        """
        Returns the type of the given letter.

        Args:
            letter (str): The letter.

        Returns:
            str: The type of the letter.
        """
        for letter_type in letter_types:
            if letter in letter_types[letter_type]:
                return letter_type
        return ""

    def get_icon_path(self, letter_type: str, letter: str) -> str:
        """
        Returns the icon path for the given letter type and letter.

        Args:
            letter_type (str): The type of the letter.
            letter (str): The letter.

        Returns:
            str: The icon path.
        """
        return f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"

    def create_button(self, icon_path: str) -> QPushButton:
        """
        Creates a button with the given icon path.

        Args:
            icon_path (str): The icon path.

        Returns:
            QPushButton: The created button.
        """
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

        button_size = int(self.main_window.width() * 0.020)
        button.setFixedSize(button_size, button_size)

        icon_size = int(button_size * 0.8)
        button.setIconSize(QSize(icon_size, icon_size))

        return button

    def update_letter_buttons_size(self) -> None:
            """
            Updates the size of the letter buttons.

            This method calculates the available width based on the main window's width and the number of letter buttons.
            It then sets the fixed size of each letter button and adjusts the icon size accordingly.
            """
            button_count = self.letter_buttons_layout.count()
            available_width = self.main_window.width() * 0.015 * 1.5 * button_count
            button_size = int(available_width / button_count)

            for i in range(button_count):
                item = self.letter_buttons_layout.itemAt(i)
                if item is not None:
                    row_layout: QHBoxLayout = item.layout()
                    for j in range(row_layout.count()):
                        button_item = row_layout.itemAt(j)
                        if button_item is not None:
                            button: QPushButton = button_item.widget()
                            button.setFixedSize(button_size, button_size)
                            icon_size = int(button_size * 0.9)
                            button.setIconSize(QSize(icon_size, icon_size))
                        
    def update_size(self) -> None:
        """
        Updates the size of the letter buttons.
        """
        self.update_letter_buttons_size()
        #set the max width of the frame to 1/6 of the option picker width
        self.setFixedWidth(int(self.option_picker.width() / 5))