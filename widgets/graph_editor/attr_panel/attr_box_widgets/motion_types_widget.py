from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QFrame,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from settings.string_constants import ICON_DIR, SWAP_ICON
from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import Colors

from widgets.graph_editor.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self._setup_ui()
        self.update_motion_type()

    def _setup_ui(self) -> None:
        # Main vertical layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        type_combo_box_frame = self.setup_combo_box_frame()

        button_frame = self.setup_button_frame()


        main_layout.addWidget(button_frame)
        main_layout.addWidget(type_combo_box_frame)

    def setup_button_frame(self) -> QFrame:
        button_frame = QFrame(self)

        # Define the layout for the button frame
        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)

        # Create the button
        self.swap_button = self._create_button()

        # Adjust the size of the button to be round
        button_size = int(self.attr_box.attr_box_width * 0.15)  # Example size
        self.swap_button.setFixedSize(button_size, button_size)

        # Add spacer to push the button up and prevent it from expanding
        button_frame_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # Add the button to the layout
        button_frame_layout.addWidget(
            self.swap_button,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        # Set fixed width for the button frame

        return button_frame

    def setup_combo_box_frame(self):
        # Header label layout
        type_header_frame = self.setup_type_header_frame()
        type_combo_box = self.setup_combo_box()

        type_combo_box_frame = QFrame(self)

        type_combo_box_frame_layout = QVBoxLayout(type_combo_box_frame)
        type_combo_box_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_combo_box_frame_layout.setContentsMargins(0, 0, 0, 0)
        type_combo_box_frame_layout.setSpacing(0)
        type_combo_box_frame_layout.addWidget(type_header_frame)
        type_combo_box_frame_layout.addWidget(type_combo_box)

        type_combo_box_frame.setFixedWidth(int(self.attr_box.attr_box_width * 3 / 4))
        return type_combo_box_frame

    def setup_type_header_frame(self):
        type_header_frame = QFrame(self)
        header_layout = QHBoxLayout()
        header_label = QLabel("Type", self)
        header_label.setFont(QFont("Arial", 12))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_label)
        type_header_frame.setLayout(header_layout)
        type_header_frame.setContentsMargins(0, 0, 0, 0)
        header_layout.setContentsMargins(0, 0, 0, 0)
        type_header_frame.setFixedHeight(int(self.attr_box.attr_box_width * 1 / 10))
        self.type_header_frame = type_header_frame
        return type_header_frame

    def setup_combo_box(self):
        type_combo_box = QComboBox(self)
        type_combo_box.addItems(["Pro", "Anti", "Dash", "Static"])
        type_combo_box.setFont(QFont("Arial", 20, QFont.Weight.Bold, True))
        type_combo_box.setStyleSheet(self.get_combo_box_style())
        type_combo_box.setFixedWidth(int(self.attr_box.attr_box_width / 2))
        self.type_combo_box = type_combo_box
        return type_combo_box

    def _create_button(self) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setStyleSheet(self.get_button_style())
        button.clicked.connect(self.swap_motion_type)
        return button

    ### HELPERS ###

    def swap_motion_type(self) -> None:
        original_motion_type_index = self.type_combo_box.currentIndex()
        # if the start index is 1
        if original_motion_type_index == 0:
            new_motion_type_index = 1
        elif original_motion_type_index == 1:
            new_motion_type_index = 0
        elif original_motion_type_index == 2:
            new_motion_type_index = 3
        elif original_motion_type_index == 3:
            new_motion_type_index = 2

        self.type_combo_box.setCurrentIndex(new_motion_type_index)
        self.update_arrow_motion_type()

    ### GETTERS ###

    def get_combo_box_style(self) -> str:
        # ComboBox style
        return (
            "QComboBox {"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
            "QComboBox::drop-down {"
            "   subcontrol-origin: padding;"
            "   subcontrol-position: top right;"
            "   width: 15px;"
            "   border-left-width: 1px;"
            "   border-left-color: darkgray;"
            "   border-left-style: solid;"
            "   border-top-right-radius: 3px;"
            "   border-bottom-right-radius: 3px;"
            "}"
            "QComboBox::down-arrow {"
            "   image: url('resources/images/icons/combobox_arrow.png');"
            "   width: 10px;"
            "   height: 10px;"
            "}"
        )

    def get_button_style(self) -> str:
        # Button style
        return (
            "QPushButton {"
            "   border-radius: 15px;"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            "   border: 1px solid black;"
            "   min-width: 30px;"
            "   min-height: 30px;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )

    ### UPDATERS ###

    def update_motion_type(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            motion_type = arrow.motion.motion_type
            index = self.type_combo_box.findText(
                motion_type.capitalize(), Qt.MatchFlag.MatchExactly
            )
            if index >= 0:
                self.type_combo_box.setCurrentIndex(index)

    def update_arrow_motion_type(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_motion_type()

    def update_motion_type_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            self.type_combo_box.height() + self.type_header_frame.height(),
        )
