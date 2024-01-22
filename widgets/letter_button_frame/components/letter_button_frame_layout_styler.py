from typing import Tuple
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import Letters


if TYPE_CHECKING:
    from widgets.letter_button_frame.letter_button_frame import LetterButtonFrame


class LetterButtonFrameLayoutStyler:
    def __init__(self, letter_button_frame: "LetterButtonFrame") -> None:
        self.spacing = letter_button_frame.spacing
        self.letter_button_frame = letter_button_frame
        self.border_colors = {
            "Type1": ("#6F2DA8", "#00b3ff"),  # Purple, Cyan
            "Type2": ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            "Type3": ("#6F2DA8", "#26e600"),  # Purple, Green
            "Type4": ("#26e600", "#26e600"),  # Green, Green
            "Type5": ("#26e600", "#00b3ff"),  # Green, Cyan
            "Type6": ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }

    def get_colors(self, type_name: str) -> Tuple[str, str]:
        return self.border_colors.get(type_name)

    def create_layout(
        self, type_name: str, row_layouts: List[QHBoxLayout]
    ) -> Tuple[QFrame, QVBoxLayout]:
        border_colors = self.get_colors(type_name)
        is_single_color = border_colors[0] == border_colors[1]

        outer_frame = self.create_styled_frame(border_colors[0], 4)
        outer_frame_layout = QVBoxLayout(outer_frame)
        outer_frame_layout.setContentsMargins(0, 0, 0, 0)
        outer_frame_layout.setSpacing(0)

        border_width = 0 if is_single_color else 4
        inner_frame = self.create_styled_frame(
            border_colors[1], border_width, outer_frame
        )
        inner_frame_layout = QVBoxLayout(inner_frame)
        inner_frame_layout.setContentsMargins(0, 0, 0, 0)
        inner_frame_layout.setSpacing(self.spacing)

        inner_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        for row_layout in row_layouts:
            row_layout.setSpacing(self.spacing)
            inner_frame_layout.addLayout(row_layout)

        outer_frame_layout.addWidget(inner_frame)
        outer_frame_layout.setStretchFactor(
            inner_frame, 1
        ) 

        return outer_frame, outer_frame_layout

    def create_styled_frame(
        self, color: str, border_width: int, parent: QFrame = None
    ) -> QFrame:
        frame = QFrame(parent)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(
            f"border: {border_width}px solid {color};" f"background-color: transparent;"
        )
        return frame


    def add_frames_to_layout(
        self, main_layout: QVBoxLayout, frame_tuples: List[Tuple[QFrame, int]]
    ) -> None:
        for frame, stretch in frame_tuples:
            main_layout.addWidget(frame, stretch)
