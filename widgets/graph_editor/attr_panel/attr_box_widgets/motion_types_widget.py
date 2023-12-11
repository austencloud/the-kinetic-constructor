from ast import main
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QComboBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont, QIcon, QResizeEvent
from PyQt6.QtCore import Qt
from settings.string_constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)

        self.motion_type_box_frame = self._setup_motion_type_box_frame()
        self.swap_button_frame = self._setup_swap_button_frame()

        # Main layout
        self._setup_main_layout()

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.swap_button_frame)
        main_layout.addWidget(self.motion_type_box_frame)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return main_layout

    def _setup_motion_type_box_frame(self) -> QFrame:
        motion_type_box_frame = QFrame(self)
        hbox_container = QHBoxLayout(motion_type_box_frame)
        layout = QVBoxLayout()
        hbox_container.setContentsMargins(0, 0, 0, 0)
        hbox_container.setSpacing(0)
        hbox_container.addStretch(1)
        hbox_container.addLayout(layout)
        hbox_container.addStretch(3)

        header_label = self.create_label(
            "Type", int(self.attr_box.attr_panel.width() / 35)
        )
        layout.addWidget(header_label)

        motion_type_box = self._setup_motion_type_box()
        layout.addWidget(motion_type_box)

        return motion_type_box_frame

    def _setup_motion_type_box(self) -> QComboBox:
        motion_type_box = QComboBox(self)
        motion_type_box.addItems(["Pro", "Anti", "Dash", "Static"])
        motion_type_box.setFont(
            QFont("Arial", int(self.attr_box.width() / 10), QFont.Weight.Bold, True)
        )
        motion_type_box.setStyleSheet(self.attr_box.get_combobox_style())
        motion_type_box.setCurrentIndex(-1)
        self.motion_type_box = motion_type_box
        return motion_type_box

    def _setup_swap_button_frame(self) -> QFrame:
        swap_button_frame = QFrame(self)
        layout = QVBoxLayout(swap_button_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        swap_button = self.create_custom_button(
            SWAP_ICON, self._swap_motion_type_callback
        )
        swap_button.setMinimumSize(
            int(self.attr_box.width() * 0.15), int(self.attr_box.width() * 0.15)
        )
        layout.addSpacerItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
        )
        layout.addWidget(
            swap_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        return swap_button_frame

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

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        common_height = max(
            widget.sizeHint().height()
            for widget in [self.swap_button_frame, self.motion_type_box_frame]
        )
        for widget in [self.swap_button_frame, self.motion_type_box_frame]:
            widget.setMaximumHeight(common_height)
        self.swap_button_frame.setMinimumWidth(int(self.attr_box.width() * 1 / 4))
        self.swap_button_frame.setMaximumWidth(int(self.attr_box.width() * 1 / 4))
        self.motion_type_box.setMinimumWidth(int(self.attr_box.width() * 0.5))
