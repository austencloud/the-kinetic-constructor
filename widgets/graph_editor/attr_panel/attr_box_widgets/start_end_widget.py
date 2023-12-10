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
        self.arrow_label = self._setup_arrow_label()

        self.start_box_with_header_frame = self._create_box_with_header_frame(
            "Start", self.start_box
        )
        self.end_box_with_header_frame = self._create_box_with_header_frame(
            "End", self.end_box
        )

        self.button_frame = self._setup_button_frame()
        self.start_to_end_frame = self._setup_start_to_end_frame()

        
        self._setup_main_layout()

        self._set_styles()

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
        frame = QFrame(self)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(
            self.start_box_with_header_frame, alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addWidget(self.arrow_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            self.end_box_with_header_frame, alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addStretch(1)  # This will push all the widgets to the left

        # Set the height of the frame to match the button frame's height
        frame.setFixedHeight(self.button_frame.height())

        return frame


    def _setup_main_layout(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.button_frame)
        self.main_layout.addWidget(self.start_to_end_frame, stretch=1)  # Make start_to_end_frame stretch to fill the space


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

    def _setup_arrow_label(self) -> QLabel:
        label = QLabel("→", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(35)
        label.setFont(font)
        label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        return label

    def _setup_button_frame(self) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)  # This will push the button to the bottom
        button = self._create_button()
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the button in the frame

        frame.setFixedWidth(int(self.attr_box.width() / 5))
        button_height = self.start_box_with_header_frame.sizeHint().height()
        frame.setFixedHeight(button_height)

        return frame
    
    def _create_button(self) -> CustomButton:
        button = CustomButton(self)
        button.setIcon(QIcon(ICON_DIR + SWAP_ICON))
        button.clicked.connect(self.swap_locations)
        return button

    def _create_box_with_header_frame(self, label_text: str, box: QComboBox) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # Remove spacing between the label and the combo box
        label = self._setup_start_end_header_label(label_text)
        layout.addWidget(label)
        layout.addWidget(box)
        frame.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        return frame

    def _setup_start_end_header_label(self, text: str) -> QLabel:
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", int(self.attr_box.attr_panel.width() / 35)))
        label.setMinimumWidth(self.start_box.sizeHint().width())
        return label



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
        self.button_frame.setFixedWidth(int(self.attr_box.width() / 5))
        # Set the height of the button frame to match the height of the start_to_end_frame
        self.button_frame.setFixedHeight(self.start_box_with_header_frame.sizeHint().height())
        self.start_to_end_frame.setFixedHeight(self.button_frame.height())
