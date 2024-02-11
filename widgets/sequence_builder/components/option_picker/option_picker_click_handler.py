from typing import TYPE_CHECKING
from ....pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class OptionPickerClickHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def get_click_handler(
        self, start_pos: "Pictograph", is_start_pos: bool
    ) -> callable:
        return lambda event: self.on_option_clicked(start_pos)

    def on_option_clicked(self, clicked_option: "Pictograph") -> None:
        self.sequence_builder.current_pictograph = clicked_option
        self.sequence_builder.option_picker.scroll_area.update_pictographs()
        new_beat = self.sequence_builder.add_to_sequence_manager.create_new_beat(
            clicked_option
        )
        self.sequence_builder.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(
            new_beat
        )
        pictograph_dict = clicked_option.get.pictograph_dict()
        new_beat.updater.update_pictograph(pictograph_dict)
        new_beat.view.is_filled = True
        self.sequence_builder.option_picker.scroll_area.display_manager.order_and_display_pictographs()
