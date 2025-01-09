from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import OptionPicker

class OptionPickerUpdater:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker

    def update_option_picker(self, sequence=None):
        if sequence is None:
            sequence = (
                self.option_picker.json_manager.loader_saver.load_current_sequence_json()
            )
        if len(sequence) > 1:
            views = [option.view for option in self.option_picker.option_pool]

            self.option_picker.fade_manager.widget_fader.fade_and_update(
                views, self._update_pictographs, 200
            )

    def _update_pictographs(self):
        sequence = (
            self.option_picker.json_manager.loader_saver.load_current_sequence_json()
        )
        selected_filter = (
            self.option_picker.reversal_filter.reversal_combobox.currentData()
        )
        next_options = self.option_picker.option_getter.get_next_options(
            sequence, selected_filter
        )
        self.option_picker.scroll_area.add_and_display_relevant_pictographs(
            next_options
        )
