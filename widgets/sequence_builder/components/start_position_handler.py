from typing import TYPE_CHECKING
from constants import END_POS, START_POS
from ...pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class StartPositionHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.start_options: dict[str, Pictograph] = {}
        self.sequence_builder = sequence_builder
        self.setup_start_positions()

    def setup_start_positions(self) -> None:
        """Shows options for the starting position."""
        self.sequence_builder.scroll_area.clear()
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_pos_option(position_key, i)

    def _on_start_pos_clicked(self, start_pos: "Pictograph") -> None:
        self.sequence_builder.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.sequence_builder.current_pictograph = start_pos
        self.sequence_builder.transition_to_sequence_building(start_pos)

    def hide_start_positions(self):
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def _add_start_pos_option(self, position_key: str, column: int) -> None:
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
                    start_option = (
                        self.sequence_builder.scroll_area.sequence_builder.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_option
                    start_option.letter = letter
                    start_option.start_pos = start_pos
                    start_option.end_pos = end_pos
                    self.sequence_builder.scroll_area._add_option_to_layout(
                        start_option, True
                    )
                    start_option.updater.update_pictograph(pictograph_dict)

    def resize_start_options(self) -> None:
        for start_option in self.start_options.values():
            start_option.view.resize_for_scroll_area()
