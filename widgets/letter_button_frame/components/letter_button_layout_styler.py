from typing import Tuple
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List

from .letter_button import LetterButton

if TYPE_CHECKING:
    from widgets.letter_button_frame.letter_button_frame import LetterButtonFrame


class LetterButtonLayoutStyler:
    def __init__(self, letter_button_frame: "LetterButtonFrame") -> None:
        self.spacing = letter_button_frame.spacing

        self.border_colors = {
            "Type1": ("#6F2DA8", "#00b3ff"),  # Purple, Cyan
            "Type2": ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            "Type3": ("#6F2DA8", "#26e600"),  # Purple, Green
            "Type4": ("#26e600", "#26e600"),  # Green, Green
            "Type5": ("#00b3ff", "#26e600"),  # Cyan, Green
            "Type6": ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }

    def get_colors(self, type_name: str) -> Tuple[str, str]:
        return self.border_colors.get(type_name, ("black", "black"))

    def create_layout(
        self, type_name: str, rows: List[List[LetterButton]]
    ) -> Tuple[QFrame, QVBoxLayout]:
        border_colors = self.get_colors(type_name)
        outer_frame = self.create_styled_frame(border_colors[0], 6)
        outer_frame_layout = QVBoxLayout(outer_frame)
        outer_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        if len(border_colors) == 2:
            inner_frame = self.create_styled_frame(border_colors[1], 3, outer_frame)
            inner_frame_layout = QVBoxLayout(inner_frame)
            inner_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            inner_frame.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            type_frame_layout = inner_frame_layout
        else:
            type_frame_layout = outer_frame_layout

        type_frame_layout.addStretch(1)

        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.setSpacing(self.spacing)
            for button in row:
                row_layout.addWidget(button)
            row_layout.addStretch(1)
            type_frame_layout.addLayout(row_layout)

        outer_frame_layout.addStretch(1)
        return outer_frame, outer_frame_layout

    def create_styled_frame(
        self, color: str, border_width: int, parent: QFrame = None
    ) -> QFrame:
        frame = QFrame(parent)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(
            f"border: {border_width}px solid {color}; "
            f"margin: {border_width}px; "
            "background-color: white;"
        )
        return frame
