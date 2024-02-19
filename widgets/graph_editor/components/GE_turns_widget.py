from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .GE_turns_box import GE_TurnsBox


class GE_TurnsWidget(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.turnbox_vbox_frame: QFrame = self._create_turnbox_vbox_frame()
        self.buttons_hbox_layout = QHBoxLayout()
        self.setup_additional_layouts()
        self._setup_layout_frames()

    def setup_additional_layouts(self) -> None:
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    ### LAYOUTS ###

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self.turn_display_and_adjust_btns_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = self._create_frame(
            self.turn_display_and_adjust_btns_hbox_layout
        )
        self.button_frame = self._create_frame(self.buttons_hbox_layout)
        self.header_frame.setContentsMargins(0, 0, 0, 0)
        self.button_frame.setContentsMargins(0, 0, 0, 0)

    def setup_additional_layouts(self):
        self.turn_display_and_adjust_btns_hbox_layout = QHBoxLayout()

    def _create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        """Creates a frame with the given layout."""
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    ### WIDGETS ###


    def _create_turnbox_vbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QVBoxLayout())

        self.turns_label = QLabel("Turns")
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turnbox_frame.layout().addWidget(self.turns_label)
        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

