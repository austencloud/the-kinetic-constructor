from typing import TYPE_CHECKING
from ....pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class OptionPickerClickHandler:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def get_click_handler(self, start_pos: "Pictograph") -> callable:
        return lambda event: self.on_option_clicked(start_pos)

    def on_option_clicked(self, clicked_option: "Pictograph") -> None:
        beat_frame = self.sequence_builder.main_widget.sequence_widget.beat_frame
        new_beat = self.sequence_builder.add_to_sequence_manager.create_new_beat(
            clicked_option
        )
        beat_frame.add_scene_to_sequence(new_beat)
        if new_beat.view:
            self.sequence_builder.option_picker.choose_your_next_pictograph_label.set_text_to_loading()
            selection_manager = beat_frame.selection_manager
            selection_manager.select_beat(new_beat.view)
            QApplication.processEvents()
            self.sequence_builder.option_picker.update_option_picker()
            new_beat.view.is_filled = True
            self.sequence_builder.option_picker.scroll_area.display_manager.order_and_display_pictographs()

            self.sequence_builder.option_picker.choose_your_next_pictograph_label.set_default_text()
