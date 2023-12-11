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
from PyQt6.QtGui import QFont, QResizeEvent, QFontMetrics
from PyQt6.QtCore import Qt
from settings.string_constants import SWAP_ICON
from utilities.TypeChecking.TypeChecking import Locations
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_combo_box import (
    CustomComboBox,
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class StartEndWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)

        # Setup start and end combo boxes
        self.start_box = self._setup_start_end_box(["N", "E", "S", "W"])
        self.end_box = self._setup_start_end_box(["N", "E", "S", "W"])

        # Setup frames for start and end combo boxes with headers
        self.start_box_with_header_frame = self._create_box_with_header_frame(
            "Start", self.start_box
        )
        self.end_box_with_header_frame = self._create_box_with_header_frame(
            "End", self.end_box
        )

        # Setup arrow label
        self.arrow_label = self.create_label("→", 35, Qt.AlignmentFlag.AlignCenter)
        self.arrow_label_frame = self._setup_arrow_label_frame(self.arrow_label)

        # Setup swap button
        self.swap_button_frame = self._setup_swap_button_frame()

        # Main layout
        self._setup_main_layout()

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.swap_button_frame)
        main_layout.addStretch(1)
        main_layout.addWidget(self.start_box_with_header_frame)
        main_layout.addWidget(self.arrow_label_frame)
        main_layout.addWidget(self.end_box_with_header_frame)
        main_layout.addStretch(3)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return main_layout

    def _setup_start_end_box(self, locations: list[str]) -> CustomComboBox:
        box = CustomComboBox(self)
        box.addItems(locations)
        box.setFont(
            QFont(
                "Arial", int(self.attr_box.attr_panel.width() / 20), QFont.Weight.Bold
            )
        )
        box.setCurrentIndex(-1)

        # Calculate the width of the widest item
        font_metrics = QFontMetrics(box.font())
        widest_char_width = font_metrics.horizontalAdvance("W")
        box.setMinimumWidth(
            int(widest_char_width * 1.75)
        )  # Adjust the multiplier as needed

        return box

    def _create_box_with_header_frame(self, label_text: str, box: QComboBox) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(
            self.create_label(label_text, int(self.attr_box.attr_panel.width() / 35))
        )
        layout.addWidget(box)
        return frame

    def _setup_arrow_label_frame(self, arrow_label: QLabel) -> QFrame:
        arrow_label_frame = QFrame(self)
        layout = QVBoxLayout(arrow_label_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)
        layout.addWidget(arrow_label, alignment=Qt.AlignmentFlag.AlignCenter)
        return arrow_label_frame

    def _setup_swap_button_frame(self) -> QFrame:
        swap_button_frame = QFrame(self)
        layout = QVBoxLayout(swap_button_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        swap_button = self.create_custom_button(
            SWAP_ICON, self._swap_locations_callback
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

    def _swap_locations_callback(self) -> None:
        start_index, end_index = (
            self.start_box.currentIndex(),
            self.end_box.currentIndex(),
        )
        self.start_box.setCurrentIndex(end_index)
        self.end_box.setCurrentIndex(start_index)

        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.arrow.swap_rot_dir()
            self.update_start_end_boxes(motion.start_location, motion.end_location)

    def update_start_end_boxes(self, start: Locations, end: Locations) -> None:
        if start and end:
            self.start_box.setCurrentText(start.upper())
            self.end_box.setCurrentText(end.upper())
        else:
            self.clear_start_end_boxes()
            
    def clear_start_end_boxes(self) -> None:
        self.start_box.setCurrentIndex(-1)
        self.end_box.setCurrentIndex(-1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        common_height = max(
            widget.sizeHint().height()
            for widget in [
                self.start_box_with_header_frame,
                self.end_box_with_header_frame,
                self.arrow_label_frame,
                self.swap_button_frame,
            ]
        )
        for widget in [
            self.start_box_with_header_frame,
            self.end_box_with_header_frame,
            self.arrow_label_frame,
            self.swap_button_frame,
        ]:
            widget.setMaximumHeight(common_height)
        self.swap_button_frame.setMinimumWidth(int(self.attr_box.width() * 1 / 4))
        self.swap_button_frame.setMaximumWidth(int(self.attr_box.width() * 1 / 4))
