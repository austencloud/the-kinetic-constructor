from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QComboBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from constants import ICON_DIR, SWAP_ICON
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import GraphEditorAttrBox


class MotionTypeWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "GraphEditorAttrBox") -> None:
        super().__init__(attr_box)

        self.header_label = self.create_attr_header_label("Type")
        self.motion_type_box: QComboBox = self._setup_motion_type_box()
        self.swap_button = self.create_attr_box_button(
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
            "anti": "Pro",
            "Dash": "Static",
            "Static": "Dash",
        }
        new_motion_type = motion_types.get(current_text, "")

        new_motion_type_index = self.motion_type_box.findText(
            new_motion_type, Qt.MatchFlag.MatchExactly
        )
        if new_motion_type_index >= 0:
            self.motion_type_box.setCurrentIndex(new_motion_type_index)
            motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion:
                motion.manipulator.swap_motion_type()

    def update_motion_type_box(self, motion_type: str) -> None:
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

    def resize_motion_type_widget(self) -> None:
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.spacing = self.attr_box.pictograph.view.width() // 250
        self.swap_button_frame.setMinimumWidth(int(self.width() * 1 / 4))
        self.swap_button_frame.setMaximumWidth(int(self.width() * 1 / 4))
        self.motion_type_box.setMinimumWidth(int(self.width() * 0.5))

        self.header_label.setFont(QFont("Arial", int(self.width() / 22)))

        self.motion_type_box.setMinimumHeight(int(self.attr_box.height() / 8))
        self.motion_type_box.setMaximumHeight(int(self.attr_box.height() / 8))
        box_font_size = int(self.width() / 10)
        self.motion_type_box.setFont(
            QFont("Arial", box_font_size, QFont.Weight.Bold, True)
        )
        self.main_vbox_frame.layout().setSpacing(
            self.attr_box.pictograph.view.width() // 100
        )
        # Update the stylesheet with the new border radius
        border_radius = (
            min(
                self.motion_type_box.width(),
                self.motion_type_box.height(),
            )
            * 0.25
        )
        self.motion_type_box.setStyleSheet(
            f"""
            QComboBox {{
                border: {self.attr_box.combobox_border}px solid black;
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
        self.header_label.setContentsMargins(0, 0, self.spacing, 0)
        self.main_vbox_frame.setMaximumHeight(self.height() + self.spacing)
        self.motion_type_box.setMaximumHeight(int(self.height() * 3 / 4 + self.spacing))
        self.header_label.setMinimumHeight(int(self.height() * 1 / 4 + self.spacing))
