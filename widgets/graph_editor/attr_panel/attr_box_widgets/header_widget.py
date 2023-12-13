from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from constants.string_constants import (
    BLUE,
    BLUE_HEX,
    RED,
    RED_HEX,
    ICON_DIR,
)
from typing import TYPE_CHECKING, Callable
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox
from constants.string_constants import ICON_DIR
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QFrame, QVBoxLayout


class HeaderWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box

        self.header_label = self._setup_header_label()
        self.rotate_cw_button = self._create_button(
            f"{ICON_DIR}rotate_cw.png", self._rotate_cw
        )
        self.rotate_ccw_button = self._create_button(
            f"{ICON_DIR}rotate_ccw.png", self._rotate_ccw
        )

        self._setup_main_layout()
        self.setMinimumWidth(self.attr_box.width())

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")  # You can adjust the color as needed
        return separator

    def _setup_main_layout(self) -> None:
        margins = self.attr_box.border_width
        main_layout = QVBoxLayout(self)  # Change to QVBoxLayout to stack vertically
        main_layout.setContentsMargins(margins, margins, margins, margins)
        main_layout.setSpacing(0)

        header_layout = QHBoxLayout()  # Use a QHBoxLayout for the header contents
        header_layout.addWidget(
            self.rotate_ccw_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )
        header_layout.addWidget(
            self.header_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        header_layout.addWidget(
            self.rotate_cw_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight,
        )

        # Add the header layout to the main layout
        main_layout.addLayout(header_layout)

        # Create and add the separator
        separator = self.create_separator()
        main_layout.addWidget(separator)

    def _rotate_ccw(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.arrow.rotate_arrow("ccw")

    def _rotate_cw(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.arrow.rotate_arrow("cw")

    def _setup_buttons(self) -> tuple[CustomButton, CustomButton]:
        rotate_ccw_button: CustomButton = self._create_button(
            f"{ICON_DIR}rotate_ccw.png"
        )
        rotate_cw_button: CustomButton = self._create_button(f"{ICON_DIR}rotate_cw.png")

        rotate_ccw_button.clicked.connect(self._rotate_ccw)
        rotate_cw_button.clicked.connect(self._rotate_cw)

        buttons = (rotate_cw_button, rotate_ccw_button)
        return buttons

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.attr_box.color == BLUE else "Right"
        color_hex = RED_HEX if self.attr_box.color == RED else BLUE_HEX
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {color_hex}; font-weight: bold;")
        return label

    def _create_button(
        self, icon_path: str, callback: Callable[[], None]
    ) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

