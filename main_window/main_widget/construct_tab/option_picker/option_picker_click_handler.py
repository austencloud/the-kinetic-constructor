# option_picker_click_handler.py

from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, pyqtSlot

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OptionPickerClickHandler:
    def __init__(self, option_picker: "OptionPicker") -> None:
        self.option_picker = option_picker

    def get_click_handler(self, start_pos: "BasePictograph") -> callable:
        return lambda event: self.on_option_clicked(start_pos)

    def on_option_clicked(self, clicked_option: "BasePictograph") -> None:
        """Handle the logic when an option is clicked."""
        beat_frame = (
            self.option_picker.construct_tab.main_widget.sequence_widget.beat_frame
        )
        new_beat = (
            self.option_picker.construct_tab.add_to_sequence_manager.create_new_beat(
                clicked_option
            )
        )
        next_beat_number = beat_frame.beat_adder.calculate_next_beat_number()
        num_beats = int(
            beat_frame.sequence_widget.main_widget.settings_manager.sequence_layout.get_layout_setting(
                "num_beats"
            )
        )

        if (
            next_beat_number > num_beats
        ) and not beat_frame.sequence_widget.main_widget.settings_manager.sequence_layout.get_layout_setting(
            "grow_sequence"
        ):
            sequence_widget = (
                self.option_picker.construct_tab.main_widget.sequence_widget
            )
            sequence_widget.indicator_label.show_message(
                f"Can't add the beat. Sequence length is set to {next_beat_number - 1} beats."
            )
            return
        beat_frame.beat_adder.add_beat_to_sequence(new_beat)

        if new_beat.view:
            self.option_picker.choose_your_next_pictograph_label.set_text_to_loading()
            selection_manager = beat_frame.selection_overlay
            selection_manager.select_beat(new_beat.view)
            QApplication.processEvents()

            # Initiate fade-out animation
            self.option_picker.update_option_picker()

            new_beat.view.is_filled = True
            self.option_picker.scroll_area.display_manager.order_and_display_pictographs()
            self.option_picker.choose_your_next_pictograph_label.set_default_text()
