from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QComboBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt
from constants.string_constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)

        self.header_label = self.create_attr_header_label("Type")
        self.motion_type_box: QComboBox = self._setup_motion_type_box()
        self.swap_button = self.create_custom_button(
            SWAP_ICON, self._swap_motion_type_callback
        )
        self.swap_button_frame = self._setup_swap_button_frame()
        self.main_vbox_frame = self._setup_main_vbox_frame()
        self._setup_main_layout()
        # self.add_black_borders()

    def add_black_borders(self) -> None:
        self.setStyleSheet("border: 1px solid black;")
        self.header_label.setStyleSheet("border: 1px solid black;")
        self.motion_type_box.setStyleSheet("border: 1px solid black;")
        self.swap_button.setStyleSheet("border: 1px solid black;")

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.swap_button_frame)
        main_layout.addWidget(self.main_vbox_frame)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_main_vbox_frame(self) -> QFrame:
        frame = QFrame(self)
        hbox = QHBoxLayout(frame)
        vbox = QVBoxLayout()

        vbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(2)

        vbox.addWidget(self.header_label)
        vbox.addWidget(self.motion_type_box)

        return frame

    def _setup_motion_type_box(self) -> QComboBox:
        box = QComboBox(self)
        box.addItems(["Pro", "Anti", "Dash", "Static"])
        box.setCurrentIndex(-1)
        return box

    def _setup_swap_button_frame(self) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.swap_button.setMinimumSize(
            int(self.attr_box.width() * 0.15), int(self.attr_box.width() * 0.15)
        )
        layout.addSpacerItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
        layout.addWidget(
            self.swap_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        return frame

    def _swap_motion_type_callback(self) -> None:
        current_text = self.motion_type_box.currentText()
        motion_types = {
            "Pro": "Anti",
            "Anti": "Pro",
            "Dash": "Static",
            "Static": "Dash",
        }
        new_motion_type = motion_types.get(current_text, "")

        new_motion_type_index = self.motion_type_box.findText(
            new_motion_type, Qt.MatchFlag.MatchExactly
        )
        if new_motion_type_index >= 0:
            self.motion_type_box.setCurrentIndex(new_motion_type_index)
            motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
            if motion:
                motion.arrow.swap_motion_type()

    def update_motion_type_box(self, motion_type: MotionTypes) -> None:
        if motion_type is None:
            self.motion_type_box.setCurrentIndex(-1)
        else:
            index = self.motion_type_box.findText(
                motion_type.capitalize(), Qt.MatchFlag.MatchExactly
            )
            if index >= 0:
                self.motion_type_box.setCurrentIndex(index)

    def clear_motion_type_box(self) -> None:
        self.motion_type_box.setCurrentIndex(-1)

