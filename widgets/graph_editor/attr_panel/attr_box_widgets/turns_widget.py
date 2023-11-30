from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFrame,
    QBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING, List, Literal

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QFrame):
    def __init__(
        self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox"
    ) -> None:
        super().__init__()
        self.pictograph = pictograph
        self.color = color
        self.attr_box = attr_box
        self.init_ui()

    def init_ui(self) -> None:
        self.setup_layouts()
        self.create_header()
        self.create_buttons_and_label()

    def setup_layouts(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.bottom_frame = QFrame(self)
        self.bottom_frame.setFixedWidth(self.attr_box.attr_box_width)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.bottom_frame)
        self.apply_layout_styles()

    def apply_layout_styles(self) -> None:
        layouts: List[QBoxLayout] = [self.layout, self.top_layout, self.bottom_layout]
        for layout in layouts:
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        self.bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_header(self) -> None:
        font = QFont("Arial", 12)
        self.turns_label_header = self._create_label("Turns", font)
        self.top_layout.addWidget(self.turns_label_header)

    def get_turns_button_style(self, button: Literal["large", "small"]) -> str:
        if button == "large":
            size = 25  # Or any other value you want for 'wide' buttons
        elif button == "small":
            size = 35  # The 'round' button size, ensuring it's the same as height

        border_radius = size / 2

        return (
            f"QPushButton {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            f"   border: 1px solid black;"
            f"   min-width: {size}px;"
            f"   min-height: {size}px;"  # Adjust height to match width for a circle
            f"   border-radius: {border_radius}px;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )

    def create_buttons_and_label(self) -> None:
        self.subtract_turn_button = self.create_button(
            "-1", self.subtract_turn_callback
        )
        self.subtract_half_turn_button = self.create_button(
            "-0.5", self.subtract_half_turn_callback
        )
        self.add_half_turn_button = self.create_button(
            "+0.5", self.add_half_turn_callback
        )
        self.add_turn_button = self.create_button("+1", self.add_turn_callback)

        # Arrange buttons with turns label in the middle
        self.bottom_layout.addWidget(self.subtract_turn_button)
        self.bottom_layout.addWidget(self.subtract_half_turn_button)

        # Add spacer to the left of the turns label
        self.bottom_layout.addItem(
            QSpacerItem(5, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.create_turns_label()

        # Add spacer to the right of the turns label
        self.bottom_layout.addItem(
            QSpacerItem(5, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.bottom_layout.addWidget(self.add_half_turn_button)
        self.bottom_layout.addWidget(self.add_turn_button)

    def create_turns_label(self) -> None:
        self.turns_label = QLabel("0", self)
        self.turns_label.setFrameShape(QFrame.Shape.Box)
        self.turns_label.setLineWidth(1)
        self.turns_label.setFrameShadow(QFrame.Shadow.Plain)
        self.turns_label.setStyleSheet(self.get_turns_label_style())
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.turns_label)

    def create_turns_label(self) -> None:
        self.turns_label = QLabel("0", self)
        self.turns_label.setFrameShape(QFrame.Shape.Box)
        self.turns_label.setLineWidth(1)
        self.turns_label.setFrameShadow(QFrame.Shadow.Plain)
        self.turns_label.setFont(
            QFont("Arial", int(self.bottom_frame.height() * 0.7), QFont.Weight.Bold)
        )
        self.turns_label.setStyleSheet(
            "background-color: white; border: 2px solid black; border-radius: 10px; letter-spacing: -2px;"
        )
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.turns_label)

    def create_button(self, text: str, callback) -> QPushButton:
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setFont(QFont("Arial", 12))
        button.setStyleSheet(self.get_button_style(text))
        return button

    def get_button_style(self, text: str) -> str:
        if text in ["+1", "-1"]:
            return self.get_turns_button_style("large")
        elif text in ["+0.5", "-0.5"]:
            return self.get_turns_button_style("small")

    def _create_label(self, text: str, font: QFont) -> QLabel:
        label = QLabel(text, self)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def add_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_turn()
            self.attr_box.update_labels(motion)

    def subtract_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_labels(motion)

    def add_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_labels(motion)

    def subtract_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_labels(motion)

    def update_turns_widget_size(self) -> None:
        self.setFixedWidth(self.attr_box.attr_box_width)
        self.turns_label.setFixedWidth(int(self.attr_box.attr_box_width / 4))
        self.setFixedHeight(
            self.turns_label_header.height() + self.bottom_frame.height()
        )
