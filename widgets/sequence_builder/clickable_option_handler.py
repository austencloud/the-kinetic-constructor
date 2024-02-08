from typing import TYPE_CHECKING
from ..pictograph.pictograph import Pictograph
if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder
from widgets.sequence_builder.sequence_builder import SequenceBuilder

class SequenceBuilderClickableOptionHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def _get_click_handler(self, option: "Pictograph", is_start_pos: bool) -> callable:
        """
        Returns a click event handler for an option. This handler updates
        the picker state based on the selected option's attributes.
        """
        if is_start_pos:
            return lambda event: self._on_start_pos_clicked(
                option,
                self.sequence_builder.filter_tab_manager.filters,
            )
        else:
            return lambda event: self._on_option_clicked(option)

    def _on_start_pos_clicked(self, start_pos: "Pictograph", attributes) -> None:
        self.sequence_builder.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.sequence_builder.main_widget.sequence_widget.beat_frame.picker_updater.emit(
            start_pos, attributes
        )

    def _on_option_clicked(self, clicked_option: "Pictograph") -> None:
        self.sequence_builder._update_pictographs(clicked_option)
        new_beat = clicked_option.add_to_sequence_manager.create_new_beat()
        self.sequence_builder.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(
            new_beat
        )
