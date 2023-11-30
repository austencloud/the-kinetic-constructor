from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
)
from PyQt6.QtGui import QIcon
from settings.string_constants import ICON_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import Locations


if TYPE_CHECKING:
    pass
from PyQt6.QtGui import QFont
from settings.string_constants import ICON_DIR, SWAP_ICON


class StartEndWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        locations: List[Locations] = ["N", "E", "S", "W"]
        
        self.startLabel = QLabel("Start:", self)
        self.startComboBox = QComboBox(self)
        self.startComboBox.addItems(locations)
        self.startComboBox.setFont(QFont("Arial", 14))  # Set the font size here

        self.swapButton = QPushButton(self)
        swap_icon_path = ICON_DIR + SWAP_ICON  # Set the icon path here
        self.swapButton.setIcon(QIcon(swap_icon_path))
        self.swapButton.clicked.connect(self.swap_locations)

        self.endLabel = QLabel("End:", self)
        self.endComboBox = QComboBox(self)

        self.endComboBox.addItems(locations)
        self.endComboBox.setFont(QFont("Arial", 14))  # Set the font size here

        self.startLayout = QVBoxLayout()
        self.startLayout.addWidget(self.startLabel)
        self.startLayout.addWidget(self.startComboBox)

        self.endLayout = QVBoxLayout()
        self.endLayout.addWidget(self.endLabel)
        self.endLayout.addWidget(self.endComboBox)

        self.layout.addLayout(self.startLayout)
        self.layout.addWidget(self.swapButton)
        self.layout.addLayout(self.endLayout)

    def swap_locations(self) -> None:
        start_index = self.startComboBox.currentIndex()
        end_index = self.endComboBox.currentIndex()
        self.startComboBox.setCurrentIndex(end_index)
        self.endComboBox.setCurrentIndex(start_index)
        self.update_locations()

    def update_locations(self) -> None:
        start_location = self.startComboBox.currentText()
        end_location = self.endComboBox.currentText()
        print(
            f"Start from objects.prop {start_location}, End from objects.prop {end_location}"
        )
