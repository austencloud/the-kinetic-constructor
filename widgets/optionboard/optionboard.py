from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from data.letter_engine_data import letter_types
from settings.string_constants import LETTER_SVG_DIR

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QFrame, QHBoxLayout


class OptionBoard(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.grid_widget = QWidget()
        self.optionboard_grid_layout = QGridLayout(self.grid_widget)
        self.main_layout = QHBoxLayout(
            self
        )  # Use QHBoxLayout to place items side by side

        self.setup_ui()
        self.populate_pictographs()
        self.connect_signals()

    def setup_ui(self) -> None:
        self.optionboard_grid_layout.setSpacing(0)
        self.main_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)

        self.setMinimumWidth(int(self.main_window.width() * 0.5))
        self.setMaximumWidth(int(self.main_window.width() * 0.5))
        self.setMinimumHeight(int(self.main_window.height() * 2 / 3))
        self.setMaximumHeight(int(self.main_window.height() * 2 / 3))
        self.setFixedSize(self.width(), self.height())
        self.init_letter_buttons_frame()
        self.init_scroll_area()

    def init_letter_buttons_frame(self) -> None:
        letter_buttons_frame = QFrame()
        letter_buttons_layout = QVBoxLayout()
        letter_buttons_layout.setSpacing(int(0))
        letter_buttons_frame.setContentsMargins(0, 0, 0, 0)
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
                button_size = int(self.main_window.width() * 0.020)
                button.setFixedSize(button_size, button_size)

                # Set icon size (slightly smaller than button for best appearance)
                icon_size = int(button_size * 0.8)  # 80% of the button size
                button.setIconSize(
                    QSize(int(button.width() * 0.8), int(button.height() * 0.8))
                )

                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)

        letter_buttons_frame.setLayout(letter_buttons_layout)
        self.letter_buttons_frame = letter_buttons_frame
        self.letter_buttons_layout = letter_buttons_layout
        self.main_layout.addWidget(letter_buttons_frame)

    def init_scroll_area(self) -> None:
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.grid_widget)
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Set the fixed width to a portion of the OptionBoard width
        scroll_area.setMinimumWidth(int(self.width() * 3 / 4))
        # Set the content margins of the scroll area and its widget to zero
        scroll_area.setContentsMargins(0, 0, 0, 0)
        self.grid_widget.setContentsMargins(0, 0, 0, 0)
        self.optionboard_grid_layout.setContentsMargins(0, 0, 0, 0)
        # Remove frame around the QScrollArea
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)

        self.main_layout.addWidget(scroll_area)
        self.scroll_area = scroll_area

    def populate_pictographs(self) -> None:
        number_of_pictographs = 50
        MAX_ITEMS_PER_ROW = 4

        # Assuming the width of the OptionBoard (self.width()) is available
        pictograph_width = (
            (self.main_widget.main_window.width() / 2) * (3 / 4) / 4
        )  # 4 pictographs per row
        pictograph_height = pictograph_width * (
            90 / 75
        )  # According to the desired ratio

        for i in range(number_of_pictographs):
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))
            pictograph_button.setIconSize(
                QSize(int(pictograph_width), int(pictograph_height))
            )
            pictograph_button.setFixedSize(
                int(pictograph_width), int(pictograph_height)
            )
            self.optionboard_grid_layout.addWidget(
                pictograph_button, i // MAX_ITEMS_PER_ROW, i % MAX_ITEMS_PER_ROW
            )

    def connect_signals(self) -> None:
        for button in self.grid_widget.findChildren(QPushButton):
            button.clicked.connect(self.on_pictograph_clicked)

    def on_pictograph_clicked(self) -> None:
        pass

    ### RESIZE EVENT HANDLERS ###

    def update_scroll_area_size(self) -> None:
        if hasattr(self, "scroll_area"):
            self.scroll_area.setMinimumWidth(int(self.width() * 3 / 4))

    def update_letter_buttons_size(self) -> None:
        if hasattr(self, "letter_buttons_frame"):
            button_size = int(self.main_window.width() * 0.020)
            for i in range(self.letter_buttons_layout.count()):
                item = self.letter_buttons_layout.itemAt(i)
                if item is not None:
                    row_layout: QHBoxLayout = item.layout()
                    for j in range(row_layout.count()):
                        button_item = row_layout.itemAt(j)
                        if button_item is not None:
                            button: QPushButton = button_item.widget()
                            button.setFixedSize(button_size, button_size)
                            button.setIconSize(
                                QSize(int(button_size * 0.8), int(button_size * 0.8))
                            )

            
            
                            
