from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFrame,
    QBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING, Dict, List, Literal

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QFrame):
    def __init__(
        self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox"
    ) -> None:
        super().__init__()
        self.pictograph = pictograph
        self.color = color
        self.attr_box = attr_box
        self._init_ui()

    def _init_ui(self) -> None:
        self.setFixedWidth(self.attr_box.attr_box_width)
        self.turnbox_frame: QFrame = self._setup_turnbox_frame()
        self.button_frames: Dict[str, QPushButton] = self._setup_button_frames()
        self.layout: QHBoxLayout = self._setup_layout()

    ### SETUP LAYOUTS ###

    def _setup_layout(self) -> QHBoxLayout:
        spacer = QSpacerItem(
            5, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_frames[self.subtract_turn_button])
        layout.addWidget(self.button_frames[self.subtract_half_turn_button])
        layout.addItem(spacer)
        layout.addWidget(self.turnbox_frame)
        layout.addItem(spacer)
        layout.addWidget(self.button_frames[self.add_half_turn_button])
        layout.addWidget(self.button_frames[self.add_turn_button])
        return layout

    ### CREATE WIDGETS ###

    def _setup_button_frame(self, button) -> QFrame:
        # set a frame so that the button is pushed down by the same amount as the height of the turns header label.
        button_frame = QFrame(self)
        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        button_frame_layout.addSpacerItem(
            QSpacerItem(
                0,
                int(self.width() / 14),
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )
        button_frame_layout.addWidget(button)
        return button_frame


    def _setup_turnbox_frame(self) -> QFrame:
        turnbox_frame = QFrame(self)
        turnbox_frame_layout = QVBoxLayout(turnbox_frame)

        self.turnbox_header = self._setup_turnbox_header()
        self.turns_label = self._create_turns_label()

        turnbox_frame_layout.addWidget(self.turnbox_header)
        turnbox_frame_layout.addWidget(self.turns_label)
        turnbox_frame_layout.setContentsMargins(0, 0, 0, 0)
        turnbox_frame_layout.setSpacing(0)
        turnbox_frame.setContentsMargins(0, 0, 0, 0)
        
        turnbox_frame.setFixedHeight(int(self.turnbox_header.height() + self.turns_label.height()))

        return turnbox_frame

    def _setup_turnbox_header(self) -> QLabel:
        turnbox_header = QLabel("Turns", self)
        turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_header.setFont(QFont("Arial", int(self.width() / 14)))
        turnbox_header.setFixedHeight(int(self.width() / 14))
        return turnbox_header

    def _setup_button_frames(self) -> list[QPushButton]:
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
        buttons = [
            self.subtract_turn_button,
            self.subtract_half_turn_button,
            self.add_half_turn_button,
            self.add_turn_button,
        ]
        
        for button in buttons:
            button_frame = self._setup_button_frame(button)
            button_frames[button] = button_frame 
               
        return button_frames

    def _create_turns_label(self) -> QLabel:
        turns_label = QLabel("0", self)
        turns_label.setFrameShape(QFrame.Shape.Box)
        turns_label.setLineWidth(1)
        turns_label.setFrameShadow(QFrame.Shadow.Plain)
        turns_label.setFont(QFont("Arial", int(self.width() / 8), QFont.Weight.Bold))
        turns_label.setStyleSheet(
            "background-color: white; border: 2px solid black; border-radius: 10px; letter-spacing: -3px;"
        )
        turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_label.setFixedHeight(int(self.attr_box.attr_box_width * 0.2) + self.turnbox_header.height())

        return turns_label

    def _create_turns_button(
        self, text: Literal["+1", "-1", "+0.5", "-0.5"], callback
    ) -> QPushButton:
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setFont(QFont("Arial", int(self.width() / 10)))
        if text in ["+1", "-1"]:
            stylesheet = self.attr_box.get_turns_button_stylesheet("small")
        elif text in ["+0.5", "-0.5"]:
            stylesheet = self.attr_box.get_turns_button_stylesheet("small")
        button.setStyleSheet(stylesheet)
        return button

    def _create_label(self, text: str, font: QFont) -> QLabel:
        label = QLabel(text, self)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

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

    def update_turns_widget_size(self) -> None:
        self.setFixedWidth(self.attr_box.attr_box_width)
        self.turns_label.setFixedWidth(int(self.attr_box.attr_box_width / 4))
        self.setFixedHeight(int(self.width() / 14) + self.turnbox_frame.height())
