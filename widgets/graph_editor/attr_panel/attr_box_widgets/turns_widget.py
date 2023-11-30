from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QWidget):
    def __init__(
        self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox"
    ) -> None:
        super().__init__()
        self.pictograph = pictograph
        self.color = color
        self.attr_box = attr_box
        self.init_ui()

    def create_button(self, text, callback) -> QPushButton:
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setFixedSize(
            30, 30
        )  # This size should be large enough to fit the text and be circular
        button.setStyleSheet(self.get_button_style())
        return button

    def get_button_style(self) -> str:
        return (
            "QPushButton {"
            "   border-radius: 15px;"  # Half of fixed size (30px / 2)
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(229, 229, 229, 255));"
            "   border: 1px solid #8f8f91;"
            "   min-width: 30px;"  # Ensures the width is not less than 30px
            "   min-height: 30px;"  # Ensures the height is not less than 30px
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )

    def init_ui(self) -> None:
        layout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setFixedHeight(
            int(self.attr_box.height() / 4)
        )  # Set a fixed height for the widget
        self.setFixedWidth(int(self.attr_box.width() - self.attr_box.border_width * 2))

        # Create buttons
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

        # Turns label
        self.turns_label = QLabel("0", self)
        self.turns_label.setFixedSize(
            int(self.attr_box.width() * 0.25), int(self.height())
        )
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_label.setStyleSheet(
            f"font-size: {int(self.attr_box.height() * 0.1)}px; font-weight: bold;"
        )

        # Add widgets to layout
        layout.addWidget(self.subtract_turn_button)
        layout.addWidget(self.subtract_half_turn_button)
        layout.addWidget(self.turns_label)
        layout.addWidget(self.add_half_turn_button)
        layout.addWidget(self.add_turn_button)

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
