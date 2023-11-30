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
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from settings.string_constants import ICON_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import Locations


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox

from settings.string_constants import ICON_DIR, SWAP_ICON
from PyQt6.QtWidgets import QSizePolicy


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

        self.label_sized_spacer = QSpacerItem(0, int(combo_box_height / 2))

        self.swap_layout = QVBoxLayout()
        self.swap_layout.addItem(self.label_sized_spacer)
        self.swap_layout.addWidget(self.swapButton)

        self.startLayout = QVBoxLayout()
        self.startLayout.addWidget(self.startLabel)
        self.startLayout.addWidget(self.startComboBox)

        self.arrow_layout = QVBoxLayout()
        self.arrow_layout.addItem(self.label_sized_spacer)
        self.arrow_layout.addWidget(self.arrow_label)

        self.endLayout = QVBoxLayout()
        self.endLayout.addWidget(self.endLabel)
        self.endLayout.addWidget(self.endComboBox)

        self.locations_layout = QHBoxLayout()
        self.locations_layout.addLayout(self.startLayout)
        self.locations_layout.addLayout(self.arrow_layout)
        self.locations_layout.addLayout(self.endLayout)
        self.locations_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.swap_layout_parent = QHBoxLayout()
        self.swap_layout_parent.addLayout(self.swap_layout)
        self.swap_layout_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.swap_layout_parent.setStretch(0, 1)  # Set swap layout to 1/4 of the width
        self.swap_layout_parent.setStretch(1, 3)  # Set other layout to 3/4 of the width

        self.layout.addLayout(self.swap_layout_parent)
        self.layout.addLayout(self.locations_layout)

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
