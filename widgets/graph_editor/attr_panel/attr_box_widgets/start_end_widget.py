from typing import TYPE_CHECKING, List
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
from constants.string_constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import Locations
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class StartEndWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)

        # Setup start and end combo boxes
        self.start_box: QComboBox = self._setup_start_end_box()
        self.end_box: QComboBox = self._setup_start_end_box()
        self.boxes: List[QComboBox] = [self.start_box, self.end_box]
        self.header_labels: List[QLabel] = []

        # Setup frames for start and end combo boxes with headers
        self.start_box_with_header_frame = self._create_combobox_with_header_frame(
            "Start", self.start_box
        )
        self.end_box_with_header_frame = self._create_combobox_with_header_frame(
            "End", self.end_box
        )
        # Setup arrow label
        self.arrow_label = self.create_attr_header_label("→")
        self.arrow_label_frame = self._setup_arrow_label_frame(self.arrow_label)

        # Setup swap button
        self.swap_button_frame = self._setup_swap_button_frame()

        # Main layout
        self._setup_main_layout()
        # self.add_black_borders()

    def add_black_borders(self):
        self.setStyleSheet("border: 1px solid black;")
        self.start_box.setStyleSheet("border: 1px solid black;")
        self.end_box.setStyleSheet("border: 1px solid black;")
        self.arrow_label.setStyleSheet("border: 1px solid black;")
        self.swap_button.setStyleSheet("border: 1px solid black;")

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

    def _setup_start_end_box(self) -> QComboBox:
        box = QComboBox(self)
        box.addItems(["N", "E", "S", "W"])
        box.setCurrentIndex(-1)
        return box

    def _create_combobox_with_header_frame(
        self, label_text: str, box: QComboBox
    ) -> QFrame:
        frame = QFrame(self)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        header_label = self.create_attr_header_label(label_text)
        layout.addWidget(header_label)
        layout.addWidget(box)
        self.header_labels.append(header_label)
        return frame

    def _setup_arrow_label_frame(self, arrow_label: QLabel) -> QFrame:
        arrow_label_frame = QFrame(self)
        layout = QVBoxLayout(arrow_label_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.arrow_spacer_label = QLabel()
        self.arrow_spacer_label.setMinimumHeight(self.header_labels[0].height())
        self.arrow_spacer_label.setMaximumHeight(self.header_labels[0].height())

        layout.addWidget(self.arrow_spacer_label)
        layout.addWidget(arrow_label)

        return arrow_label_frame

    def _setup_swap_button_frame(self) -> QFrame:
        swap_button_frame = QFrame(self)
        layout = QVBoxLayout(swap_button_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.swap_button = self.create_custom_button(
            SWAP_ICON, self._swap_locations_callback
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
        if self.size() != event.oldSize():
            self.update_size_and_styles()

    def update_size_and_styles(self):
        self.swap_button_frame.setMinimumWidth(int(self.attr_box.width() * 1 / 4))
        self.swap_button_frame.setMaximumWidth(int(self.attr_box.width() * 1 / 4))

        self.arrow_label.setMinimumHeight(self.start_box.height())
        self.arrow_label.setMaximumHeight(self.start_box.height())

        self.arrow_spacer_label.setMinimumHeight(self.header_labels[0].height())
        self.arrow_spacer_label.setMaximumHeight(self.header_labels[0].height())
        for header_label in self.header_labels:
            header_label.setFont(QFont("Arial", int(self.attr_box.width() / 18)))
        self.arrow_label.setFont(
            QFont(
                "Arial",
                int(self.attr_box.width() / 10),
                QFont.Weight.Bold,
            )
        )

        for box in self.boxes:
            box.setFont(
                QFont(
                    "Arial",
                    int(self.attr_box.attr_panel.width() / 20),
                    QFont.Weight.Bold,
                )
            )

            box.setMinimumWidth(int(self.attr_box.width() / 3.5))
            box.setMaximumWidth(int(self.attr_box.width() / 3.5))
            box.setMinimumHeight(int(self.attr_box.width() / 5))
            box.setMaximumHeight(int(self.attr_box.width() / 5))

            box_font_size = int(self.attr_box.width() / 10)
            box.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold, True))

            # Calculate the border radius as a fraction of the width or height
            border_radius = (
                min(box.width(), box.height()) * 0.25
            )  # Adjust the factor as needed

            # Update the stylesheet with the new border radius
            box.setStyleSheet(
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
