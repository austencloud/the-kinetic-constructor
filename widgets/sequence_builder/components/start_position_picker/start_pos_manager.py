from copy import deepcopy
from PyQt6.QtCore import QObject, pyqtSignal
from constants import END_POS, START_POS
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import (
    StartPositionBeatView,
    StartPositionBeat,
)
from ....pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__()
        self.sequence_builder = start_pos_picker.sequence_builder
        self.start_pos_picker = start_pos_picker
        self.start_pos_frame = start_pos_picker.pictograph_frame
        self.start_options: dict[str, Pictograph] = {}
        self.setup_start_positions()

    def setup_start_positions(self) -> None:
        """Shows options for the starting position."""
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_position(position_key)

    def _add_start_position(self, position_key: str) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for (
            letter,
            pictograph_dicts,
        ) in self.sequence_builder.main_widget.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_position_pictograph = (
                        self.start_pos_picker.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_position_pictograph
                    start_position_pictograph.letter = letter
                    start_position_pictograph.start_pos = start_pos
                    start_position_pictograph.end_pos = end_pos
                    self.start_pos_frame._add_start_pos_to_layout(
                        start_position_pictograph
                    )
                    start_position_pictograph.updater.update_pictograph(pictograph_dict)

                    start_position_pictograph.view.mousePressEvent = (
                        lambda event: self.on_start_pos_clicked(
                            start_position_pictograph
                        )
                    )

    def on_start_pos_clicked(self, clicked_start_option: Pictograph):
        start_position_beat = StartPositionBeat(
            self.sequence_builder.main_widget,
            self.sequence_builder.main_widget.sequence_widget.beat_frame,
        )
        start_position_beat.updater.update_pictograph(
            deepcopy(clicked_start_option.pictograph_dict)
        )

        self.sequence_builder.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos_beat(
            start_position_beat
        )

        self.sequence_builder.current_pictograph = start_position_beat

        self.start_position_selected.connect(
            self.sequence_builder.transition_to_sequence_building
        )
        self.sequence_builder.main_widget.json_manager.current_sequence_json_handler.set_start_position_data(
            start_position_beat
        )
        self.start_position_selected.emit(start_position_beat)
        # start_position_beat.add_start_text()

    def hide_start_positions(self):
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def resize_start_position_pictographs(self):
        spacing = 10
        for start_option in self.start_options.values():
            view_width = int((self.start_pos_frame.width() // 6) - spacing)
            start_option.view.setFixedSize(view_width, view_width)
            start_option.view.view_scale = view_width / start_option.width()
            start_option.view.resetTransform()
            start_option.view.scale(
                start_option.view.view_scale, start_option.view.view_scale
            )
            start_option.container.styled_border_overlay.resize_styled_border_overlay()
