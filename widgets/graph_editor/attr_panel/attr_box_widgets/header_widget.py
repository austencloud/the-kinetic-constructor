from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from settings.string_constants import BLUE, BLUE_HEX, RED, RED_HEX, ICON_DIR
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING
from objects.arrow import Arrow


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox
from settings.string_constants import ICON_DIR



class HeaderWidget(QWidget):
    def __init__(self, attr_box: "AttrBox", color: Colors) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.color = color
        self.arrow: Arrow = self.attr_box.pictograph.get_arrow_by_color(self.color)

    def setup_header_widget(self) -> None:
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

        self.header_text_label = QLabel("Left" if self.color == BLUE else "Right", self)
        self.header_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_text_label.setFixedSize(
            int(self.attr_box.width() * 0.5), int(self.attr_box.height() * 1/6)
        )
        color_hex = RED_HEX if self.color == RED else BLUE_HEX
        font_size = int(self.header_text_label.height() * 0.5)
        self.header_text_label.setStyleSheet(
            f"color: {color_hex}; font-size: {font_size}px; font-weight: bold;"
        )

        self.rotate_ccw_button = self.create_round_button(f"{ICON_DIR}rotate_left.png")
        self.rotate_cw_button = self.create_round_button(f"{ICON_DIR}rotate_right.png")

        if self.arrow:
            self.rotate_ccw_button.clicked.connect(self.arrow.rotate("ccw"))
            self.rotate_cw_button.clicked.connect(self.arrow.rotate("cw"))

        layout.addWidget(self.clock_label)
        layout.addStretch(1)
        layout.addWidget(self.header_text_label, 1)
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

    def rotate_left(self) -> None:
        # Implementation for rotating left
        pass

    def rotate_right(self) -> None:
        # Implementation for rotating right
        pass
