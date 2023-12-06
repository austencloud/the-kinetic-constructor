from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Dict, Literal

from widgets.graph_editor.attr_panel.custom_button import CustomButton


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QFrame):
    def __init__(self, attr_box: "AttrBox"):
        super().__init__()
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self.attr_box = attr_box
        self._init_ui()

    def _init_ui(self) -> None:
        self.setFixedWidth(
            self.attr_box.attr_box_width - self.attr_box.border_width * 2
        )
        self.turnbox_frame: QFrame = self._setup_turnbox_frame()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_buttons()
        # self._add_borders()

    def _add_borders(self) -> None:
        self.setStyleSheet("border: 1px solid black;")
        self.turnbox_frame.setStyleSheet("border: 1px solid black;")

    ### CREATE WIDGETS ###

    def _create_buttons(self):
        self.subtract_turn_button = self._create_turns_button(
            "-1", self._subtract_turn_callback, is_full_turn=True
        )
        self.subtract_half_turn_button = self._create_turns_button(
            "-0.5", self._subtract_half_turn_callback, is_full_turn=False
        )
        self.add_half_turn_button = self._create_turns_button(
            "+0.5", self._add_half_turn_callback, is_full_turn=False
        )
        self.add_turn_button = self._create_turns_button(
            "+1", self._add_turn_callback, is_full_turn=True
        )

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.layout.addLayout(top_layout)
        self.layout.addLayout(bottom_layout)

        top_layout.addWidget(self.turnbox_frame)

        bottom_layout.addWidget(self.subtract_turn_button)
        bottom_layout.addWidget(self.subtract_half_turn_button)
        bottom_layout.addWidget(self.add_half_turn_button)
        bottom_layout.addWidget(self.add_turn_button)

    def _setup_button_frame(self, full_turn_button, half_turn_button) -> QFrame:
        # set a frame so that the buttons are stacked vertically
        button_frame = QFrame(self)
        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        button_frame_layout.addWidget(full_turn_button)
        button_frame_layout.addWidget(half_turn_button)
        return button_frame

    def _setup_turnbox_frame(self) -> QFrame:
        turnbox_frame = QFrame(self)
        turnbox_layout = QVBoxLayout(turnbox_frame)
        turnbox_layout.setContentsMargins(0, 0, 0, 0)
        turnbox_frame.setContentsMargins(0, 0, 0, 0)
        turnbox_layout.setSpacing(0)
        self.turnbox_header = QLabel("Turns", self)
        self.turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turnbox_header.setFont(QFont("Arial", int(self.width() / 14)))
        self.turns_label = self._create_turns_label()
        turnbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_layout.addWidget(self.turnbox_header)
        turnbox_layout.addWidget(self.turns_label)

        return turnbox_frame

    def _setup_turns_header(self) -> QLabel:
        turnbox_header = QLabel("Turns", self)
        turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_header.setFont(QFont("Arial", int(self.width() / 14)))
        turnbox_header.setFixedHeight(int(self.width() / 14))
        return turnbox_header

    def _setup_button_frames(self) -> Dict[str, QFrame]:
        button_frames = {}

        self.subtract_turn_button = self._create_turns_button(
            "-1", self._subtract_turn_callback
        )
        self.subtract_half_turn_button = self._create_turns_button(
            "-0.5", self._subtract_half_turn_callback
        )
        self.add_half_turn_button = self._create_turns_button(
            "+0.5", self._add_half_turn_callback
        )
        self.add_turn_button = self._create_turns_button("+1", self._add_turn_callback)

        subtract_button_frame = self._setup_button_frame(
            self.subtract_turn_button, self.subtract_half_turn_button
        )
        add_button_frame = self._setup_button_frame(
            self.add_turn_button, self.add_half_turn_button
        )

        button_frames["subtract_buttons"] = subtract_button_frame
        button_frames["add_buttons"] = add_button_frame

        return button_frames

    def _create_turns_label(self) -> QLabel:
        turns_label = QLabel("", self)
        turns_label.setFrameShape(QFrame.Shape.Box)
        turns_label.setLineWidth(1)
        turns_label.setFrameShadow(QFrame.Shadow.Plain)
        turns_label.setFont(QFont("Arial", int(self.width() / 8), QFont.Weight.Bold))
        turns_label.setStyleSheet(
            "background-color: white; border: 2px solid black; border-radius: 10px; letter-spacing: -2px;"
        )
        turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_label.setFixedSize(
            int(self.attr_box.attr_box_width * 0.3),
            int(self.attr_box.attr_box_width * 0.2),
        )
        turns_label.setContentsMargins(0, 0, 0, 0)
        return turns_label

    def _create_turns_button(
        self, text: Literal["+1", "-1", "+0.5", "-0.5"], callback, is_full_turn: bool
    ) -> CustomButton:
        button_size = int(self.attr_box.attr_box_width * 0.2)
        if not is_full_turn:
            button_size = int(button_size * 0.75)  # Half turn buttons are smaller

        button = CustomButton(self)
        button.setText(text)
        button.setFont(
            QFont("Arial", int(button_size / 3))
        )  # Adjust font size based on button size
        button.setFixedSize(button_size, button_size)
        button.clicked.connect(callback)

        return button

    def _add_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_turn()
            self.attr_box.update_labels(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_labels(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_labels(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_labels(motion)

    ### UPDATERS ###


    def update_turns_label_box(self, motion):
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion and motion.turns is not None:
            self.turns_label.setText(str(motion.turns))
        else:
            self.turns_label.setText("")

    def clear_turns_label(self) -> None:
        self.turns_label.setText("")

    def update_turns_widget_size(self) -> None:
        self.setFixedWidth(
            self.attr_box.attr_box_width - self.attr_box.border_width * 2
        )
