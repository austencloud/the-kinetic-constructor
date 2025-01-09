from typing import TYPE_CHECKING
from utilities.reversal_detector import ReversalDetector
from Enums.Enums import LetterType
from base_widgets.base_pictograph.base_pictograph import BasePictograph

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionUpdater:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.scroll_area = option_picker.option_scroll

    def refresh_options(self, sequence=None):
        if sequence is None:
            sequence = (
                self.option_picker.json_manager.loader_saver.load_current_sequence_json()
            )

        if len(sequence) > 1:
            views = [option.view for option in self.option_picker.option_pool]
            self.option_picker.fade_manager.widget_fader.fade_and_update(
                views, self.update_options, 200
            )

    def update_options(self):
        option_picker = self.option_picker
        sequence = option_picker.json_manager.loader_saver.load_current_sequence_json()
        selected_filter = option_picker.reversal_filter.reversal_combobox.currentData()
        next_options = option_picker.option_getter.get_next_options(
            sequence, selected_filter
        )
        for section in self.option_picker.option_scroll.sections.values():
            section.clear_pictographs()

        for i, pictograph_dict in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                break
            pictograph = self.option_picker.option_pool[i]
            pictograph.updater.update_pictograph(pictograph_dict)
            section = self.scroll_area.sections[
                LetterType.get_letter_type(pictograph.letter)
            ]
            pictograph.view.update_borders()
            if section:
                section.add_pictograph(pictograph)
