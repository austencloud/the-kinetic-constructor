from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import SequenceBeatFrame


class SequenceButtonFrame(QFrame):
    def __init__(
        self,
        main_widget: "MainWidget",
        beat_frame: "SequenceBeatFrame",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.beat_frame = beat_frame
        self.button_height = int(self.main_widget.height() * 1 / 20)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.buttons = []
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.buttons.append(self.clear_sequence_button)

        self.layout.addWidget(self.clear_sequence_button)
