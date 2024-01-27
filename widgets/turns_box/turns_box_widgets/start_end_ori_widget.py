from typing import TYPE_CHECKING, list
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QComboBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from constants import ICON_DIR
from utilities.TypeChecking.TypeChecking import Orientations
from widgets.turns_box.turns_box_widgets.base_attr_box_widget import TurnsBoxWidget


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import GraphEditorTurnsBox


class StartEndOriWidget(TurnsBoxWidget):
    def __init__(self, turns_box: "GraphEditorTurnsBox") -> None:
        super().__init__(turns_box)

        # Setup start and end combo boxes
        self.start_ori_box: QComboBox = self._setup_ori_box()
        self.end_ori_box: QComboBox = self._setup_ori_box()
        self.ori_boxes: list[QComboBox] = [self.start_ori_box, self.end_ori_box]
        self.header_labels: list[QLabel] = []

        # Setup frames for start and end combo boxes with headers
        self.start_ori_box_with_header_frame = self._create_vbox_with_header_frame(
            "Start", self.start_ori_box
        )
        self.end_ori_box_with_header_frame = self._create_vbox_with_header_frame(
            "End", self.end_ori_box
        )
        # Setup arrow label
        self.arrow_label = self.create_attr_header_label("→")
        self.arrow_label_frame = self._setup_arrow_label_frame(self.arrow_label)

        # Main layout
        self._setup_main_layout()
        # self.add_black_borders()

    def add_black_borders(self):
        self.setStyleSheet("border: 1px solid black;")
        self.start_ori_box.setStyleSheet("border: 1px solid black;")
        self.end_ori_box.setStyleSheet("border: 1px solid black;")
        self.arrow_label.setStyleSheet("border: 1px solid black;")

    def _setup_main_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch(1)
        main_layout.addWidget(self.start_ori_box_with_header_frame)
        main_layout.addWidget(self.arrow_label_frame)
        main_layout.addWidget(self.end_ori_box_with_header_frame)
        main_layout.addStretch(3)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return main_layout

    def _setup_ori_box(self) -> QComboBox:
        box = QComboBox(self)
        box.addItems(["N", "E", "S", "W"])
        box.setCurrentIndex(-1)
        return box

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

    def update_start_end_boxes(
        self, start_ori: Orientations, end_ori: Orientations
    ) -> None:
        if start_ori and end_ori:
            self.start_ori_box.setCurrentText(start_ori.upper())
            self.end_ori_box.setCurrentText(end_ori.upper())
        else:
            self.clear_start_end_boxes()

    def clear_start_end_boxes(self) -> None:
        self.start_ori_box.setCurrentIndex(-1)
        self.end_ori_box.setCurrentIndex(-1)

    def resize_start_end_widget(self) -> None:
        self.setMinimumWidth(self.turns_box.width() - self.turns_box.border_width * 2)
        self.setMaximumWidth(self.turns_box.width() - self.turns_box.border_width * 2)

        self.arrow_label.setMinimumHeight(self.start_ori_box.height())
        self.arrow_label.setMaximumHeight(self.start_ori_box.height())

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

        for ori_box in self.ori_boxes:
            box_font_size = int(self.width() / 10)
            ori_box.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

            ori_box.setMinimumWidth(int(self.width() / 3.5))
            ori_box.setMaximumWidth(int(self.width() / 3.5))

            ori_box.setMinimumHeight(int(self.turns_box.height() / 8))
            ori_box.setMaximumHeight(int(self.turns_box.height() / 8))

            border_radius = min(ori_box.width(), ori_box.height()) * 0.25

            ori_box.setStyleSheet(
                f"""
                QComboBox {{
                    padding-left: 2px; /* add some padding on the left for the text */
                    padding-right: 0px; /* make room for the arrow on the right */
                    border: {self.turns_box.combobox_border}px solid black;
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
