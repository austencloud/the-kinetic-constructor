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
from settings.string_constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_combo_box import (
    CustomComboBox,
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)

        self.motion_type_box_frame = self._setup_main_frame()
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

    def _setup_main_frame(self) -> QFrame:
        motion_type_box_frame = QFrame(self)
        main_frame_hbox_container = QHBoxLayout(motion_type_box_frame)
        self.main_frame_vbox_layout = QVBoxLayout()
        main_frame_hbox_container.setContentsMargins(0, 0, 0, 0)
        main_frame_hbox_container.setSpacing(0)
        main_frame_hbox_container.addStretch(1)
        main_frame_hbox_container.addLayout(self.main_frame_vbox_layout)
        main_frame_hbox_container.addStretch(3)

        self.header_label = self.create_attr_header_label("Type")
        self.motion_type_box = self._setup_motion_type_box()

        self.main_frame_vbox_layout.addWidget(self.header_label)
        self.main_frame_vbox_layout.addWidget(self.motion_type_box)

        return motion_type_box_frame

    def _setup_motion_type_box(self) -> CustomComboBox:
        motion_type_box = CustomComboBox(self)
        motion_type_box.addItems(["Pro", "Anti", "Dash", "Static"])
        motion_type_box.setCurrentIndex(-1)
        return motion_type_box

    def _setup_swap_button_frame(self) -> QFrame:
        swap_button_frame = QFrame(self)
        layout = QVBoxLayout(swap_button_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.swap_button = self.create_custom_button(
            SWAP_ICON, self._swap_motion_type_callback
        )
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
        self.swap_button.update_button_size()
        header_font_size = int(self.attr_box.pictograph.view.width() * 0.06)
        self.header_label.setFont(QFont("Arial", header_font_size))
        self.motion_type_box.setMinimumHeight(int(self.attr_box.width() / 5))
        self.motion_type_box.setMaximumHeight(int(self.attr_box.width() / 5))
        box_font_size = int(self.attr_box.width() / 10)
        self.motion_type_box.setFont(
            QFont("Arial", box_font_size, QFont.Weight.Bold, True)
        )
        self.main_frame_vbox_layout.setSpacing(
            self.attr_box.pictograph.view.width() // 100
        )
        # Update the stylesheet with the new border radius
        border_radius = (
            min(self.motion_type_box.width(), self.motion_type_box.height()) * 0.25
        )
        self.motion_type_box.setStyleSheet(
            f"""
            QComboBox {{
                border: {self.motion_type_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}

            QComboBox::down-arrow {{
                image: url("{ICON_DIR}combobox_arrow.png");
                width: 10px;
                height: 10px;
            }}
            """
        )
