from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QSpacerItem,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from settings.string_constants import ICON_DIR
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import Locations, Colors


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    

from settings.string_constants import ICON_DIR, SWAP_ICON


class StartEndWidget(QWidget):
    def __init__(self, pictograph: 'Pictograph', color:Colors, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.pictograph = pictograph
        self.color = color

        locations: List[Locations] = ["N", "E", "S", "W"]
        
        font = QFont("Arial", 14, weight=QFont.Weight.Bold)
        arrow_font = QFont("Arial", 20, weight=QFont.Weight.Bold) 
        
        combo_box_height = 30
        arrow_extra_width = 10 

        self.start_label = QLabel("Start:", self)
        self.start_label.setFixedHeight(int(combo_box_height / 2))
        self.start_combo_box = QComboBox(self)
        self.start_combo_box.addItems(locations)
        self.start_combo_box.setFont(font)
        self.start_combo_box.setFixedSize(
            combo_box_height + arrow_extra_width, combo_box_height
        )
        self.label_sized_spacer = QSpacerItem(0, int(combo_box_height / 2))
        self.arrow_label = QLabel("→", self)
        self.arrow_label.setFixedHeight(int(combo_box_height / 2))
        self.arrow_label.setFont(arrow_font)  # Set the font to bold

        self.swap_button = QPushButton(self)
        swap_icon_path = ICON_DIR + SWAP_ICON
        self.swap_button.setIcon(QIcon(swap_icon_path))
        self.swap_button.setFixedSize(
            combo_box_height, combo_box_height
        )  # Keep the button add_
        self.swap_button.clicked.connect(self.swap_locations)

        self.end_label = QLabel("End:", self)
        self.end_label.setFixedHeight(int(combo_box_height / 2))
        self.end_combo_box = QComboBox(self)
        self.end_combo_box.addItems(locations)
        self.end_combo_box.setFont(font)
        self.end_combo_box.setFixedSize(
            combo_box_height + arrow_extra_width, combo_box_height
        )

        self.wide_spacer = QSpacerItem(int(combo_box_height/2), int(combo_box_height))

        self.swap_layout = QVBoxLayout()
        self.swap_layout.addItem(self.label_sized_spacer)
        self.swap_layout.addWidget(self.swap_button)

        self.spacer_layout = QVBoxLayout()
        self.spacer_layout.addItem(self.wide_spacer)

        self.start_layout = QVBoxLayout()
        self.start_layout.addWidget(self.start_label)
        self.start_layout.addWidget(self.start_combo_box)

        self.arrow_layout = QVBoxLayout()
        self.arrow_layout.addItem(self.label_sized_spacer)
        self.arrow_layout.addWidget(self.arrow_label)

        self.end_layout = QVBoxLayout()
        self.end_layout.addWidget(self.end_label)
        self.end_layout.addWidget(self.end_combo_box)

        self.locations_layout = QHBoxLayout()
        self.locations_layout.addLayout(self.start_layout)
        self.locations_layout.addLayout(self.arrow_layout)
        self.locations_layout.addLayout(self.end_layout)
        self.locations_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.swap_layout_parent = QHBoxLayout()
        self.swap_layout_parent.addLayout(self.swap_layout)
        self.swap_layout_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(self.swap_layout_parent)
        self.layout.addLayout(self.spacer_layout)
        self.layout.addLayout(self.locations_layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def swap_locations(self) -> None:
        start_index = self.start_combo_box.currentIndex()
        end_index = self.end_combo_box.currentIndex()
        self.start_combo_box.setCurrentIndex(end_index)
        self.end_combo_box.setCurrentIndex(start_index)
        self.update_arrow_rotation_direction()


    def update_combo_boxes(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            start_location = motion.start_location.upper()
            end_location = motion.end_location.upper()
            self.start_combo_box.setCurrentText(start_location)
            self.end_combo_box.setCurrentText(end_location)

    def update_arrow_rotation_direction(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_rot_dir()
