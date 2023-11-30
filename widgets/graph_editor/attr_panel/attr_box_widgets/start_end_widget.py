from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon
from settings.string_constants import ICON_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import Locations


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox

from PyQt6.QtGui import QFont
from settings.string_constants import ICON_DIR, SWAP_ICON


class StartEndWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        locations: List[Locations] = ["N", "E", "S", "W"]
        font = QFont("Arial", 14)

        # Adjust these sizes as necessary
        combo_box_height = 30  # Height for the combo box
        arrow_extra_width = 10  # Additional width for the dropdown arrow

        self.startLabel = QLabel("Start:", self)
        self.startLabel.setFixedHeight(int(combo_box_height / 2))
        self.startComboBox = QComboBox(self)
        self.startComboBox.addItems(locations)
        self.startComboBox.setFont(font)
        self.startComboBox.setFixedSize(
            combo_box_height + arrow_extra_width, combo_box_height
        )

        self.arrow_label = QLabel("→", self)
        self.arrow_label.setFixedHeight(int(combo_box_height / 2))
        self.arrow_label.setFont(font)

        self.swapButton = QPushButton(self)
        swap_icon_path = ICON_DIR + SWAP_ICON
        self.swapButton.setIcon(QIcon(swap_icon_path))
        self.swapButton.setFixedSize(
            combo_box_height, combo_box_height
        )  # Keep the button add_
        self.swapButton.clicked.connect(self.swap_locations)

        self.endLabel = QLabel("End:", self)
        self.endLabel.setFixedHeight(int(combo_box_height / 2))
        self.endComboBox = QComboBox(self)
        self.endComboBox.addItems(locations)
        self.endComboBox.setFont(font)
        self.endComboBox.setFixedSize(
            combo_box_height + arrow_extra_width, combo_box_height
        )

        self.spacer = QSpacerItem(
            0, int(combo_box_height / 2), QSizePolicy.Policy.Expanding
        )

        self.swapLayout = QVBoxLayout()
        self.swapLayout.addItem(self.spacer)
        self.swapLayout.addWidget(self.swapButton)

        self.startLayout = QVBoxLayout()
        self.startLayout.addWidget(self.startLabel)
        self.startLayout.addWidget(self.startComboBox)

        self.arrow_layout = QVBoxLayout()
        self.arrow_layout.addItem(self.spacer)
        self.arrow_layout.addWidget(self.arrow_label)

        self.endLayout = QVBoxLayout()
        self.endLayout.addWidget(self.endLabel)
        self.endLayout.addWidget(self.endComboBox)

        self.layout.addLayout(self.swapLayout)
        self.layout.addLayout(self.startLayout)
        self.layout.addLayout(self.arrow_layout)
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
