from typing import TYPE_CHECKING
from constants import END_POS, START_POS
from ..pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from .sequence_builder_scroll_area import SequenceBuilderScrollArea


class StartPositionHandler:
    def __init__(self, scroll_area: "SequenceBuilderScrollArea") -> None:
        self.scroll_area = scroll_area
        self.letters = scroll_area.main_widget.letters
        self.start_options: dict[str, Pictograph] = {}

    def setup_start_position(self) -> None:
        """Shows options for the starting position."""
        self.scroll_area.clear()
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_pos_option(position_key, i)

    def _add_start_pos_option(self, position_key: str, column: int) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for letter, pictograph_dicts in self.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_option = (
                        self.scroll_area.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_option
                    start_option.letter = letter
                    start_option.start_pos = start_pos
                    start_option.end_pos = end_pos
                    self.scroll_area._add_option_to_layout(start_option, True)
                    start_option.updater.update_pictograph(pictograph_dict)

    def resize_start_options(self) -> None:
        for start_option in self.start_options.values():
            start_option.view.resize_for_scroll_area()
