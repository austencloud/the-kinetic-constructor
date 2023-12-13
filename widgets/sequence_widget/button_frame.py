from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame


class ButtonFrame(QFrame):
    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        beat_frame: "BeatFrame",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = pictograph
        self.beat_frame = beat_frame
        self.button_height = int(self.main_widget.height() * 1 / 20)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = []
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.buttons.append(self.clear_sequence_button)

        self.layout.addWidget(self.clear_sequence_button)

    def resizeEvent(self, event) -> None:
        self.setMaximumHeight(self.button_height)
        self.setMaximumWidth(self.beat_frame.beats[0].width())
        self.clear_sequence_button.setMinimumHeight(self.button_height)
