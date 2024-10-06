from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
        ManualBuilder,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OptionPickerClickHandler:
    def __init__(self, manual_builder: "ManualBuilder") -> None:
        self.manual_builder = manual_builder

    def get_click_handler(self, start_pos: "BasePictograph") -> callable:
        return lambda event: self.on_option_clicked(start_pos)

    def on_option_clicked(self, clicked_option: "BasePictograph") -> None:
        beat_frame = (
            self.manual_builder.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        new_beat = self.manual_builder.add_to_sequence_manager.create_new_beat(
            clicked_option
        )
        beat_frame.beat_adder.add_beat_to_sequence(new_beat)
        if new_beat.view:
            self.manual_builder.option_picker.choose_your_next_pictograph_label.set_text_to_loading()
            selection_manager = beat_frame.selection_overlay
            selection_manager.select_beat(new_beat.view)
            QApplication.processEvents()
            self.manual_builder.option_picker.update_option_picker()
            new_beat.view.is_filled = True
            self.manual_builder.option_picker.scroll_area.display_manager.order_and_display_pictographs()
            self.manual_builder.option_picker.choose_your_next_pictograph_label.set_default_text()
