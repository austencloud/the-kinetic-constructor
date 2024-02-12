from PyQt6.QtCore import QObject, pyqtSignal
from constants import END_POS, START_POS
from ....pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosManager(QObject):
    start_position_selected = pyqtSignal(Pictograph)

    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__()  # Initialize the QObject base class
        self.sequence_builder = start_pos_picker.sequence_builder
        self.scroll_area = start_pos_picker.scroll_area
        self.start_options: dict[str, Pictograph] = {}
        self.setup_start_positions()

    def setup_start_positions(self) -> None:
        """Shows options for the starting position."""
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_pos_option(position_key)

    def _add_start_pos_option(self, position_key: str) -> None:
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
                        self.scroll_area.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_position_pictograph
                    start_position_pictograph.letter = letter
                    start_position_pictograph.start_pos = start_pos
                    start_position_pictograph.end_pos = end_pos
                    self.scroll_area._add_start_pos_to_layout(
                        start_position_pictograph, True
                    )
                    start_position_pictograph.updater.update_pictograph(pictograph_dict)

                    start_position_pictograph.view.mousePressEvent = (
                        lambda event: self.on_start_pos_clicked(
                            start_position_pictograph
                        )
                    )

    def on_start_pos_clicked(self, start_position_pictograph: Pictograph):
        self.sequence_builder.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_position_pictograph
        )
        self.sequence_builder.current_pictograph = start_position_pictograph

        self.start_position_selected.connect(
            self.sequence_builder.transition_to_sequence_building
        )
        self.sequence_builder.main_widget.sequence_widget.sequence_validation_engine.add_to_sequence(
            start_position_pictograph
        )
        self.start_position_selected.emit(start_position_pictograph)

    def hide_start_positions(self):
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def resize_start_position_pictographs(self):
        spacing = 10
        for start_option in self.start_options.values():
            view_width = int(
                (self.scroll_area.width() / self.scroll_area.COLUMN_COUNT) - spacing
            )
            start_option.view.setFixedSize(view_width, view_width)
            start_option.view.view_scale = view_width / start_option.width()
            start_option.view.resetTransform()
            start_option.view.scale(
                start_option.view.view_scale, start_option.view.view_scale
            )
            start_option.container.styled_border_overlay.resize_styled_border_overlay()
