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
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from constants import ICON_DIR, SWAP_ICON
from utilities.TypeChecking.TypeChecking import Locations
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )


class StartEndLocWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "GraphEditorAttrBox") -> None:
        super().__init__(attr_box)

        # Setup start and end combo boxes
        self.start_loc_box: QComboBox = self._setup_loc_box()
        self.end_loc_box: QComboBox = self._setup_loc_box()
        self.loc_boxes: List[QComboBox] = [self.start_loc_box, self.end_loc_box]
        self.header_labels: List[QLabel] = []

        # Setup frames for start and end combo boxes with headers
        self.start_loc_box_with_header_frame = self._create_vbox_with_header_frame(
            "Start", self.start_loc_box
        )
        self.end_loc_box_with_header_frame = self._create_vbox_with_header_frame(
            "End", self.end_loc_box
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
        self.start_loc_box.setStyleSheet("border: 1px solid black;")
        self.end_loc_box.setStyleSheet("border: 1px solid black;")
        self.arrow_label.setStyleSheet("border: 1px solid black;")
        self.swap_button.setStyleSheet("border: 1px solid black;")

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.swap_button_frame)
        main_layout.addStretch(1)
        main_layout.addWidget(self.start_loc_box_with_header_frame)
        main_layout.addWidget(self.arrow_label_frame)
        main_layout.addWidget(self.end_loc_box_with_header_frame)
        main_layout.addStretch(3)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return main_layout

    def _setup_loc_box(self) -> QComboBox:
        loc_box = QComboBox(self)
        loc_box.addItems(["N", "E", "S", "W"])
        loc_box.setCurrentIndex(-1)
        return loc_box

    def _create_vbox_with_header_frame(self, label_text: str, box: QComboBox) -> QFrame:
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

        self.swap_button = self.create_attr_box_button(
            SWAP_ICON, self._swap_locations_callback
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
            self.start_loc_box.currentIndex(),
            self.end_loc_box.currentIndex(),
        )
        self.start_loc_box.setCurrentIndex(end_index)
        self.end_loc_box.setCurrentIndex(start_index)

        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.manipulator.swap_rot_dir()
            self.update_start_end_loc_boxes(motion.start_loc, motion.end_loc)

    def update_start_end_loc_boxes(
        self, start_loc: Locations, end_loc: Locations
    ) -> None:
        if start_loc and end_loc:
            self.start_loc_box.setCurrentText(start_loc.upper())
            self.end_loc_box.setCurrentText(end_loc.upper())
        else:
            self.clear_start_end_boxes()

    def clear_start_end_boxes(self) -> None:
        self.start_loc_box.setCurrentIndex(-1)
        self.end_loc_box.setCurrentIndex(-1)

    def resize_start_end_widget(self) -> None:
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.swap_button_frame.setMaximumWidth(int(self.width() * 1 / 4))
        self.swap_button_frame.setMinimumWidth(int(self.width() * 1 / 4))

        self.arrow_label.setMinimumHeight(self.start_loc_box.height())
        self.arrow_label.setMaximumHeight(self.start_loc_box.height())

        self.arrow_spacer_label.setMinimumHeight(self.header_labels[0].height())
        self.arrow_spacer_label.setMaximumHeight(self.header_labels[0].height())

        for header_label in self.header_labels:
            header_label.setFont(QFont("Arial", int(self.width() / 22)))
        self.arrow_label.setFont(
            QFont(
                "Arial",
                int(self.width() / 10),
                QFont.Weight.Bold,
            )
        )
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow

        for loc_box in self.loc_boxes:
            box_font_size = int(self.width() / 10)
            loc_box.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

            loc_box.setMinimumWidth(int(self.width() / 3.5))
            loc_box.setMaximumWidth(int(self.width() / 3.5))

            loc_box.setMinimumHeight(int(self.attr_box.height() / 8))
            loc_box.setMaximumHeight(int(self.attr_box.height() / 8))

            border_radius = min(loc_box.width(), loc_box.height()) * 0.25

            loc_box.setStyleSheet(
                f"""
                QComboBox {{
                    padding-left: 2px; /* add some padding on the left for the text */
                    padding-right: 0px; /* make room for the arrow on the right */
                    border: {self.attr_box.combobox_border}px solid black;
                    border-radius: {border_radius}px;
                }}
                QComboBox::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: {dropdown_arrow_width}px;
                    border-left-width: 1px;
                    border-left-color: darkgray;
                    border-left-style: solid; /* visually separate the arrow part */
                    border-top-right-radius: {border_radius}px;
                    border-bottom-right-radius: {border_radius}px;
                }}
                QComboBox::down-arrow {{
                    image: url("{ICON_DIR}/combobox_arrow.png");
                    width: {int(dropdown_arrow_width * 0.6)}px;
                    height: {int(dropdown_arrow_width * 0.6)}px;
                }}
            """
            )
