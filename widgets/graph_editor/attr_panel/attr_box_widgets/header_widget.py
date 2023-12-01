from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from settings.string_constants import BLUE, BLUE_HEX, RED, RED_HEX, ICON_DIR
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING
from objects.motion import Motion
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox
from settings.string_constants import ICON_DIR


class HeaderWidget(QWidget):
    def __init__(self, attr_box: "AttrBox", color: Colors) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.color = color
        
        self.motion: Motion = self.attr_box.pictograph.get_motion_by_color(self.color)
        self.clock: QLabel = self._setup_clock()
        self.header_text:QLabel = self._setup_header_text()
        self.rotate_cw_button, self.rotate_ccw_button = self._setup_buttons()
        
        self._setup_main_layout()

    def _setup_main_layout(self) -> QHBoxLayout:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.clock)
        main_layout.addWidget(self.header_text)
        main_layout.addWidget(self.rotate_ccw_button)
        main_layout.addWidget(self.rotate_cw_button)
        
        return main_layout

    def _setup_clock(self) -> QLabel:
        clock = QLabel(self)
        clock_pixmap = QPixmap(f"{ICON_DIR}clock/clockwise.png")
        if clock_pixmap.isNull():
            print("Failed to load the clock icon.")
        else:
            clock.setPixmap(
                clock_pixmap.scaled(
                    int(self.attr_box.width() / 4),
                    int(self.attr_box.width() / 4),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        return clock

    def _setup_buttons(self) -> tuple[CustomButton, CustomButton]:
        rotate_ccw_button = self.create_round_button(f"{ICON_DIR}rotate_left.png")
        rotate_cw_button = self.create_round_button(f"{ICON_DIR}rotate_right.png")
        if self.motion:
            rotate_ccw_button.clicked.connect(self.motion.arrow.rotate("ccw"))
            rotate_cw_button.clicked.connect(self.motion.arrow.rotate("cw"))
        buttons = (rotate_ccw_button, rotate_cw_button)
        return buttons

    def _setup_header_text(self) -> QLabel:
        header_text = QLabel("Left" if self.color == BLUE else "Right", self)
        header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_text.setFixedSize(
            int(self.attr_box.width() * 0.5), int(self.attr_box.height() * 1 / 6)
        )
        color_hex = RED_HEX if self.color == RED else BLUE_HEX
        font_size = int(header_text.height() * 0.5)
        header_text.setStyleSheet(
            f"color: {color_hex}; font-size: {font_size}px; font-weight: bold;"
        )
        return header_text

    def create_round_button(self, icon_path: str) -> CustomButton:
        button = CustomButton(self)
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

    def update_header_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            int(self.attr_box.height() * 1 / 6),
        )
