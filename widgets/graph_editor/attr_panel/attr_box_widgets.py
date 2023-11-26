from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QVBoxLayout,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from settings.string_constants import BLUE, BLUE_HEX, ICON_PATHS, RED, RED_HEX, ICON_DIR
from utilities.TypeChecking.TypeChecking import Color
from typing import TYPE_CHECKING
from objects.arrow import Arrow


if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


from PyQt6.QtCore import QSize


class HeaderWidget(QWidget):
    def __init__(self, attr_box: "AttrBox", color: Color) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.color = color
        self.arrow: Arrow = self.attr_box.graphboard.get_arrow_by_color(self.color)

    def setup_header_widget(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Clock label
        self.clock_label = QLabel(self)
        clock_pixmap = QPixmap(f"{ICON_DIR}clock/clockwise.png")
        if clock_pixmap.isNull():
            print("Failed to load the clock icon.")
        else:
            self.clock_label.setPixmap(
                clock_pixmap.scaled(
                    int(self.attr_box.width() / 4),
                    int(self.attr_box.width() / 4),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        self.header_label = QLabel("Left" if self.color == BLUE else "Right", self)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setFixedSize(
            int(self.attr_box.width() * 0.5), int(self.attr_box.height() * 0.25)
        )
        color_hex = RED_HEX if self.color == RED else BLUE_HEX
        font_size = int(self.header_label.height() * 0.5)
        self.header_label.setStyleSheet(
            f"color: {color_hex}; font-size: {font_size}px; font-weight: bold;"
        )

        self.rotate_ccw_button = self.create_round_button(f"{ICON_DIR}rotate_left.png")
        self.rotate_cw_button = self.create_round_button(f"{ICON_DIR}rotate_right.png")



        if self.arrow:
            self.rotate_ccw_button.clicked.connect(self.arrow.rotate("ccw"))
            self.rotate_cw_button.clicked.connect(self.arrow.rotate("cw"))

        layout.addWidget(self.clock_label)
        layout.addStretch(1)
        layout.addWidget(self.header_label, 1)
        layout.addStretch(1)
        layout.addWidget(self.rotate_ccw_button)
        layout.addWidget(self.rotate_cw_button)

        self.setLayout(layout)

    def create_round_button(self, icon_path: str) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button_size = 25  # Example size, adjust as needed
        button.setIconSize(QSize(int(button_size * 0.8), int(button_size * 0.8)))
        button.setFixedSize(int(button_size), int(button_size))

        return button

    def rotate_left(self):
        # Implementation for rotating left
        pass

    def rotate_right(self):
        # Implementation for rotating right
        pass


class MotionTypeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.motion_type = "Pro"
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.typeLabel = QLabel("Type:", self)
        self.typeButton = QPushButton(self.motion_type, self)
        self.typeButton.clicked.connect(self.toggle_motion_type)

        self.layout.addWidget(self.typeLabel)
        self.layout.addWidget(self.typeButton)

    def toggle_motion_type(self):
        if self.motion_type == "Pro":
            self.motion_type = "Anti"
        elif self.motion_type == "Anti":
            self.motion_type = "Pro"
        elif self.motion_type == "Static":
            pass

        self.typeButton.setText(self.motion_type)
        self.update_motion_type(self.motion_type)

    def update_motion_type(self, motion_type):
        print(f"Motion type set to: {motion_type}")


class StartEndWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.startLabel = QLabel("Start:", self)
        self.startComboBox = QComboBox(self)
        self.startComboBox.addItems(["N", "E", "S", "W"])

        self.swapButton = QPushButton("Swap", self)
        self.swapButton.clicked.connect(self.swap_locations)

        self.endLabel = QLabel("End:", self)
        self.endComboBox = QComboBox(self)
        self.endComboBox.addItems(["N", "E", "S", "W"])

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
        print(f"Start location: {start_location}, End location: {end_location}")


class TurnsWidget(QWidget):
    def __init__(
        self, graphboard: "GraphBoard", color: Color, attr_box: "AttrBox"
    ) -> None:
        super().__init__()
        self.graphboard = graphboard
        self.color = color
        self.attr_box = attr_box
        self.init_ui()

    def init_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Reduced spacing between widgets

        self.setFixedHeight(int(self.attr_box.height() * 0.25))
        self.setFixedWidth(int(self.attr_box.width()))
        # Create spacers that will push the buttons and label to the center
        left_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        right_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.subtract_turns_button = QPushButton(self)
        self.subtract_turns_button.setIcon(QIcon(ICON_PATHS["subtract_turns"]))
        self.subtract_turns_button.clicked.connect(self.subtract_turns_callback)
        self.subtract_turns_button.setFixedSize(30, 30)
        self.subtract_turns_button.setStyleSheet(
            "border-radius: 15px;"
        )  # Set the border-radius to half of the width

        self.turns_label = QLabel("0", self)
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_label.setStyleSheet(
            f"font-size: {int(self.attr_box.height() * 0.1)}px;"
        )  # Set the font size dynamically

        self.add_turns_button = QPushButton(self)
        # Apply a stylesheet to make the button round and stylized
        self.add_turns_button.setStyleSheet(
            "QPushButton {"
            "   border-radius: %dpx;"  # Half of the button size for a perfect circle
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(229, 229, 229, 255));"
            "   border: 1px solid #8f8f91;"
            "   min-width: %dpx;"
            "   min-height: %dpx;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
            % (
                self.attr_box.button_size // 2,
                self.attr_box.button_size,
                self.attr_box.button_size,
            )
        )
        self.add_turns_button.setIcon(QIcon(ICON_PATHS["add_turns"]))
        self.add_turns_button.setIconSize(self.attr_box.icon_size)
        self.add_turns_button.clicked.connect(self.add_turns_callback)
        self.add_turns_button.setStyleSheet(
            "border-radius: 15px;"
        )  # Set the border-radius to half of the width

        # Add the spacers and widgets to the layout
        layout.addItem(left_spacer)
        layout.addWidget(self.subtract_turns_button)
        layout.addWidget(self.turns_label)
        layout.addWidget(self.add_turns_button)
        layout.addItem(right_spacer)

    def subtract_turns_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.subtract_turn()
            self.attr_box.update_labels(arrow)

    def add_turns_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.add_turn()
            self.attr_box.update_labels(arrow)
