from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QFrame,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from settings.string_constants import ICON_DIR, SWAP_ICON
from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self._setup_ui()
        self.update_motion_type_box()

    def _setup_ui(self) -> None:
        # Main vertical layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(self.attr_box.attr_box_width)
        
        motion_type_box_frame = self._setup_motion_type_box_frame()
        button_frame = self._setup_button_frame()

        main_layout.addWidget(button_frame)
        main_layout.addWidget(motion_type_box_frame)

    def _setup_button_frame(self) -> QFrame:
        swap_button = self._create_button()
        button_frame = QFrame(self)

        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)

        button_size = int(self.attr_box.attr_box_width * 0.15)  # Example size
        swap_button.setFixedSize(button_size, button_size)
        button_frame_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        button_frame_layout.addWidget(
            swap_button,
            0,
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter,
        )

        return button_frame

    def _setup_motion_type_box_frame(self):
        # Header label layout
        type_header_frame = self._setup_type_header_frame()
        typebox = self._setup_typebox()
        self.spacing = int(self.attr_box.attr_box_width * 0.01)
        motion_type_box_frame = QFrame(self)
        motion_type_box_frame_layout = QVBoxLayout(motion_type_box_frame)
        motion_type_box_frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        motion_type_box_frame_layout.setContentsMargins(0, 0, 0, 0)
        motion_type_box_frame_layout.setSpacing(self.spacing)
        motion_type_box_frame_layout.addWidget(type_header_frame)
        motion_type_box_frame_layout.addWidget(typebox)

        motion_type_box_frame.setFixedWidth(int(self.attr_box.attr_box_width * 3 / 4))

        return motion_type_box_frame

    def _setup_type_header_frame(self):
        motion_type_header_frame = QFrame(self)
        motion_type_header_layout = QHBoxLayout()

        # Header label
        motion_type_header_label = QLabel("Type", self)
        motion_type_header_label.setFont(QFont("Arial", int(self.width() / 14)))
        motion_type_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        motion_type_header_layout.addWidget(motion_type_header_label)
        motion_type_header_layout.setContentsMargins(0, 0, 0, 0)

        motion_type_header_frame.setLayout(motion_type_header_layout)
        motion_type_header_frame.setContentsMargins(0, 0, 0, 0)
        motion_type_header_frame.setFixedHeight(int(self.attr_box.attr_box_width * 1 / 10))
        
        self.type_header_frame = motion_type_header_frame
        return motion_type_header_frame

    def _setup_typebox(self):
        motion_type_box = QComboBox(self)
        motion_type_box.addItems(["Pro", "Anti", "Dash", "Static"])
        motion_type_box.setFont(QFont("Arial", int(self.width() / 10), QFont.Weight.Bold, True))
        motion_type_box.setStyleSheet(self.attr_box.get_combobox_style())
        motion_type_box.setFixedWidth(int(self.attr_box.attr_box_width * 0.6))
        motion_type_box.setFixedHeight(int(self.attr_box.attr_box_width * 0.2))
        self.motion_type_box = motion_type_box
        return motion_type_box

    def _create_button(self) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.setStyleSheet(self.attr_box.get_button_style())
        button.clicked.connect(self._swap_motion_type_callback)
        return button

    ### HELPERS ###

    def _swap_motion_type_callback(self) -> None:
        original_motion_type_index = self.motion_type_box.currentIndex()
        # if the start index is 1
        if original_motion_type_index == 0:
            new_motion_type_index = 1
        elif original_motion_type_index == 1:
            new_motion_type_index = 0
        elif original_motion_type_index == 2:
            new_motion_type_index = 3
        elif original_motion_type_index == 3:
            new_motion_type_index = 2

        self.motion_type_box.setCurrentIndex(new_motion_type_index)
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.arrow.swap_motion_type()

    ### UPDATERS ###

    def update_motion_type_box(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion_type = motion.motion_type
            index = self.motion_type_box.findText(
                motion_type.capitalize(), Qt.MatchFlag.MatchExactly
            )
            if index >= 0:
                self.motion_type_box.setCurrentIndex(index)

    def update_motion_type_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            self.motion_type_box.height() + self.type_header_frame.height() + self.spacing,
        )
