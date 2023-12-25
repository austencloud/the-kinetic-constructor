from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Callable
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor_tab.attr_panel.attr_box import AttrBox
from constants.string_constants import BLUE, HEX_BLUE, HEX_RED, ICON_DIR, RED
from PyQt6.QtWidgets import QFrame, QVBoxLayout


class HeaderWidget(AttrBoxWidget):
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

        self.buttons = [self.rotate_cw_button, self.rotate_ccw_button]
        self._setup_main_layout()
        self.setMinimumWidth(self.attr_box.width())
        # self.add_black_borders()

    def add_black_borders(self):
        self.setStyleSheet("border: 1px solid black;")
        self.header_label.setStyleSheet("border: 1px solid black;")
        self.rotate_cw_button.setStyleSheet("border: 1px solid black;")
        self.rotate_ccw_button.setStyleSheet("border: 1px solid black;")

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")  # You can adjust the color as needed
        separator.setMaximumWidth(self.attr_box.width())
        return separator

    def _setup_main_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove all content margins
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch(1)
        header_layout.addWidget(self.rotate_ccw_button)
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.rotate_cw_button)
        header_layout.addStretch(1)

        self.separator = self.create_separator()

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _rotate_ccw(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.arrow.manipulator.rotate_arrow("ccw")

    def _rotate_cw(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.arrow.manipulator.rotate_arrow("cw")

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.attr_box.color == BLUE else "Right"
        color_hex = HEX_RED if self.attr_box.color == RED else HEX_BLUE
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

    def _update_button_size(self) -> None:
        for button in self.buttons:
            button.setFont(QFont("Arial", int(button.height() / 3)))

    def resize_header_widget(self) -> None:
        self.separator.setMaximumWidth(
            self.attr_box.width() - self.attr_box.border_width * 2
        )
        self.header_label.setFont(QFont("Arial", int(self.height() / 3)))
        self._update_button_size()
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
