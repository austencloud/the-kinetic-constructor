from typing import TYPE_CHECKING

from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionUpdater:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker

    def refresh_options(self, sequence=None):
        if sequence is None:
            sequence = (
                self.option_picker.json_manager.loader_saver.load_current_sequence_json()
            )

        if len(sequence) > 1:
            views = [option.view for option in self.option_picker.option_pool]
            self.option_picker.fade_manager.widget_fader.fade_and_update(
                views, self._update_options, 200
            )

    def _update_options(self):
        option_picker = self.option_picker
        sequence = option_picker.json_manager.loader_saver.load_current_sequence_json()
        selected_filter = option_picker.reversal_filter.reversal_combobox.currentData()
        next_options = option_picker.option_getter.get_next_options(
            sequence, selected_filter
        )
        self.add_and_display_relevant_options(next_options)

    def add_and_display_relevant_options(self, next_options: list[dict]):
        for section in self.option_picker.option_scroll.sections.values():
            section.clear_pictographs()

        for i, pictograph_dict in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                break
            pictograph = self.option_picker.option_pool[i]
            pictograph.updater.update_pictograph(pictograph_dict)
            sequence_so_far = (
                self.option_picker.json_manager.loader_saver.load_current_sequence_json()
            )
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_dict
            )
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)
            self.option_picker.option_scroll.display_manager.add_pictograph_to_section(
                pictograph
            )
            pictograph.view.update_borders()
