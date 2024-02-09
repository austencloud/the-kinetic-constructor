from typing import TYPE_CHECKING
from ....pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class StartPosPickerClickHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def get_click_handler(
        self, start_pos: "Pictograph", is_start_pos: bool
    ) -> callable:
        """
        Returns a click event handler for an option. This handler updates
        the picker state based on the selected option's attributes.
        """
        if is_start_pos:
            return lambda event: self.sequence_builder.start_position_picker.on_start_pos_clicked(
                start_pos
            )
        else:
            return lambda event: self._on_option_clicked(start_pos)

    def _on_option_clicked(self, clicked_option: "Pictograph") -> None:
        self.sequence_builder.option_picker.scroll_area.update_pictographs(
            clicked_option
        )
        new_beat = clicked_option.add_to_sequence_manager.create_new_beat()
        self.sequence_builder.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(
            new_beat
        )
