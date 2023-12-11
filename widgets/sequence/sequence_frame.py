from typing import TYPE_CHECKING, List

from PyQt6.QtWidgets import (
    QGridLayout,
    QFrame,
)


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.sequence.sequence_widget import SequenceWidget

from widgets.sequence.beat_view import BeatView


class Sequence(QFrame):
    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        sequence_widget: "SequenceWidget",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = pictograph
        self.sequence = sequence_widget
        self.beats: List[BeatView] = []

        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        for j in range(4):
            for i in range(4):
                beat_view = BeatView()
                self.layout.addWidget(beat_view, j, i)
                self.beats.append(beat_view)

    def update_size(self) -> None:
        self.setMinimumHeight(
            int(self.main_widget.height() - self.sequence.buttons.height())
        )
        beat_height = int(((self.height() / 4)))
        beat_width = int(beat_height * 75 / 90)

        self.sequence.setMinimumWidth(beat_width * 4)

        for beat in self.beats:
            beat.setMinimumHeight(beat_height)
            beat.setMinimumWidth(beat_width)

    def add_scene_to_sequence(self, copied_scene: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beats[next_beat_index].set_pictograph(copied_scene)

    def find_next_available_beat(self) -> int:
        # Implement logic to find the next available beat
        for i, beat in enumerate(self.beats):
            if (
                beat.scene() is None or beat.scene().items() == []
            ):  # Check if the beat is empty
                return i
        return None  # Return None if all beats are full
