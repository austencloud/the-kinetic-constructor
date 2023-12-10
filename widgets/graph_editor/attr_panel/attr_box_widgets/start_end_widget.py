from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont, QIcon, QResizeEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QComboBox,
    QSpacerItem,
)

from settings.string_constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import Locations
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_combo_box import (
    CustomComboBox,
)
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class StartEndWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(parent=attr_box)
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self.attr_box = attr_box

        self._init_ui()

    def _init_ui(self) -> None:
        self.start_box = self._setup_start_end_box()
        self.end_box = self._setup_start_end_box()
        self.arrow_label_frame = self._setup_arrow_label_frame()

        self.start_box_with_header_frame = self._create_box_with_header_frame(
            "Start", self.start_box
        )
        self.end_box_with_header_frame = self._create_box_with_header_frame(
            "End", self.end_box
        )

        self.button_frame = self._setup_button_frame()
        self.start_to_end_frame = self._setup_start_to_end_frame()

        self.main_layout = self._setup_main_layout()

        # self._set_styles()

    def _set_styles(self) -> None:
        style = "border: 1px solid black;"
        for widget in [
            self,
            self.button_frame,
            self.start_box_with_header_frame,
            self.end_box_with_header_frame,
        ]:
            widget.setStyleSheet(style)

    def _setup_start_to_end_frame(self) -> QFrame:
        start_to_end_frame = QFrame(self)
        start_to_end_frame_layout = QHBoxLayout(start_to_end_frame)
        start_to_end_frame_layout.setContentsMargins(0, 0, 0, 0)

        # Add stretch to the left
        start_to_end_frame_layout.addStretch(1)

        # Add start frame
        start_to_end_frame_layout.addWidget(
            self.start_box_with_header_frame, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Add arrow label frame without stretching
        start_to_end_frame_layout.addWidget(self.arrow_label_frame)

        # Add end frame
        start_to_end_frame_layout.addWidget(self.end_box_with_header_frame)

        # Add stretch to the right
        start_to_end_frame_layout.addStretch(4)

        start_to_end_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_to_end_frame_layout.setSpacing(0)

        return start_to_end_frame

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.button_frame)
        main_layout.addWidget(
            self.start_to_end_frame, stretch=1
        )  # Make start_to_end_frame stretch to fill the space
        return main_layout

    def _setup_start_end_box(self) -> CustomComboBox:
        box = CustomComboBox(self)
        box.addItems(["N", "E", "S", "W"])
        box.setFont(
            QFont(
                "Arial", int(self.attr_box.attr_panel.width() / 20), QFont.Weight.Bold
            )
        )
        box.setCurrentIndex(-1)
        box.setMinimumSize(box.sizeHint())
        return box

    def _setup_arrow_label_frame(self) -> QFrame:
        arrow_label_frame = QFrame(self)
        arrow_label_frame_layout = QVBoxLayout(arrow_label_frame)
        arrow_label_frame_layout.setContentsMargins(0, 0, 0, 0)
        arrow_label_frame_layout.addStretch(
            1
        )  # This will push the arrow label to the bottom, aligning it with the button and combo boxes
        self.arrow_label = self._setup_arrow_label(arrow_label_frame)
        arrow_label_frame_layout.addWidget(
            self.arrow_label, alignment=Qt.AlignmentFlag.AlignCenter
        )  # Center the arrow label in the frame

        return arrow_label_frame

    def _setup_arrow_label(self, arrow_label_frame):
        arrow_label = QLabel("→", arrow_label_frame)
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = arrow_label.font()
        font.setPointSize(35)
        arrow_label.setFont(font)
        arrow_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        return arrow_label

    def _setup_button_frame(self) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)  # This will push the button to the bottom
        button = self._create_button()
        layout.addWidget(
            button, alignment=Qt.AlignmentFlag.AlignCenter
        )  # Center the button in the frame

        frame.setMinimumWidth(int(self.attr_box.width() / 5))
        button_height = self.start_box_with_header_frame.sizeHint().height()
        frame.setMinimumHeight(button_height)

        return frame

    def _create_button(self) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.clicked.connect(self.swap_locations)
        return button

    def _create_box_with_header_frame(self, label_text: str, box: QComboBox) -> QFrame:
        box_with_header_frame = QFrame(self)
        box_with_header_frame_layout = QVBoxLayout(box_with_header_frame)
        box_with_header_frame_layout.setContentsMargins(0, 0, 0, 0)
        box_with_header_frame_layout.setSpacing(
            0
        )  # Remove spacing between the label and the combo box

        self.start_end_header_label = self._setup_start_end_header_label(label_text)
        box_with_header_frame_layout.addWidget(self.start_end_header_label)
        box_with_header_frame_layout.addWidget(box)

        box_with_header_frame.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )

        return box_with_header_frame

    def _setup_start_end_header_label(self, text: str) -> QLabel:
        start_end_header_label = QLabel(text, self)
        start_end_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_end_header_label.setFont(
            QFont("Arial", int(self.attr_box.attr_panel.width() / 35))
        )
        start_end_header_label.setMinimumWidth(self.start_box.sizeHint().width())
        return start_end_header_label

    def swap_locations(self) -> None:
        self.start_box, self.end_box = self.end_box, self.start_box
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.arrow.swap_rot_dir()

    def clear_start_end_boxes(self) -> None:
        self.start_box.setCurrentIndex(-1)
        self.end_box.setCurrentIndex(-1)

    def update_start_end_boxes(self, start: Locations, end: Locations) -> None:
        for location, box in zip([start, end], [self.start_box, self.end_box]):
            box.setCurrentIndex(
                -1 if location is None else box.findText(location.upper())
            )

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        # Set the fixed width for the button frame based on the attr_box width
        self.button_frame.setMinimumWidth(int(self.attr_box.width() / 5))
        # Set the fixed height for the button and arrow label frames based on the height of the start_box_with_header_frame
        common_height = self.start_box_with_header_frame.sizeHint().height()
        self.button_frame.setMinimumHeight(common_height)
        self.start_to_end_frame.setMinimumHeight(common_height)
        self.arrow_label.setMinimumHeight(
            common_height - self.start_end_header_label.height()
        )
        self.arrow_label_frame.setMinimumHeight(
            self.start_box_with_header_frame.sizeHint().height()
        )  # Match the height with the button and combo boxes
