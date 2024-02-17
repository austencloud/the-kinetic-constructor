from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
from PyQt6.QtCore import Qt

from Enums.letters import LetterType

if TYPE_CHECKING:
    from widgets.codex.codex_letter_button_frame.codex_letter_button_frame import (
        CodexLetterButtonFrame,
    )


class LetterButtonFrameLayoutStyler:
    def __init__(self, letter_button_frame: "CodexLetterButtonFrame") -> None:
        self.spacing = letter_button_frame.spacing
        self.letter_button_frame = letter_button_frame
        self.border_colors = {
            LetterType.Type1: ("#6F2DA8", "#00b3ff"),  # Purple, Cyan
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#6F2DA8", "#26e600"),  # Purple, Green
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#26e600", "#00b3ff"),  # Green, Cyan
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }

    def get_colors(self, type_name: str) -> tuple[str, str]:
        border_colors = self.border_colors.get(type_name)
        if border_colors[0] == border_colors[1]:
            border_colors = (border_colors[0], "transparent")
        return border_colors

    def create_layout(self, type_name: str, row_layouts: list[QHBoxLayout]) -> QFrame:
        border_colors = self.get_colors(type_name)
        outer_frame, outer_layout = self._setup_outer_frame(border_colors)
        inner_frame, inner_layout = self._setup_inner_frame(border_colors)
        type_label_frame = self._setup_type_label_frame(type_name, inner_frame)
        self._add_frames_to_layout(
            row_layouts, outer_layout, inner_frame, inner_layout, type_label_frame
        )
        return outer_frame, outer_layout

    def _add_frames_to_layout(
        self,
        row_layouts,
        outer_layout: QVBoxLayout,
        inner_frame,
        inner_layout: QVBoxLayout,
        type_label_frame,
    ):
        inner_layout.addWidget(type_label_frame, 0)
        for row_layout in row_layouts:
            inner_layout.addLayout(row_layout)
        outer_layout.addWidget(inner_frame, 1)

    def _setup_outer_frame(self, border_colors):
        outer_frame = self.create_styled_frame(border_colors[0], 4)
        outer_layout = QVBoxLayout(outer_frame)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        return outer_frame, outer_layout

    def _setup_inner_frame(self, border_colors):
        inner_frame = self.create_styled_frame(border_colors[1], 4)
        inner_layout = QVBoxLayout(inner_frame)
        inner_layout.setContentsMargins(5, 5, 5, 5)
        inner_layout.setSpacing(self.spacing)
        return inner_frame, inner_layout

    def _setup_type_label_frame(self, letter_type: LetterType, inner_frame):
        type_label = self.create_type_label(letter_type.value[-1][-1])
        type_label_frame = QFrame(inner_frame)
        type_label_frame.setStyleSheet("border: none;")
        type_label_frame.setMaximumHeight(16)
        type_label_layout = QVBoxLayout(type_label_frame)
        type_label_layout.addWidget(type_label)
        type_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_label_layout.setContentsMargins(0, 0, 0, 0)
        type_label_layout.setSpacing(0)
        return type_label_frame

    def add_label_and_buttons_to_main_frame(
        self, main_layout: QVBoxLayout, type_num_frame, buttons_frame
    ) -> None:
        main_layout.addWidget(type_num_frame)
        main_layout.addWidget(buttons_frame)
        main_layout.setStretchFactor(buttons_frame, 1)

    def _create_main_frame(self) -> tuple[QFrame, QVBoxLayout]:
        main_frame = QFrame()
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        return main_frame, main_layout

    def _create_buttons_frame(
        self, row_layouts: list[QHBoxLayout], border_colors
    ) -> QFrame:
        buttons_frame = self.create_styled_frame(border_colors[1], 4)
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(5, 0, 5, 5)  # Margins for the buttons frame
        for row_layout in row_layouts:
            row_layout.setSpacing(self.spacing)
            buttons_layout.addLayout(row_layout)
        return buttons_frame

    def create_type_label(self, type_number: str) -> QLabel:
        label = QLabel(type_number)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-weight: bold; font-size: 16px; border: none;")
        return label

    def create_styled_frame(
        self, color: str, border_width: int, parent: QFrame = None
    ) -> QFrame:
        frame = QFrame(parent)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(
            f"border: {border_width}px solid {color}; background-color: transparent;"
        )
        return frame

    def add_frames_to_layout(
        self, main_layout: QVBoxLayout, frame_tuples: list[tuple[QFrame, int]]
    ) -> None:
        for frame, stretch in frame_tuples:
            main_layout.addWidget(frame, stretch)
