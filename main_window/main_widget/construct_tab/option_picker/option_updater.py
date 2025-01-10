from typing import TYPE_CHECKING, Callable, Any
import cProfile
import pstats
import os
import tempfile
from io import TextIOWrapper

from Enums.letters import LetterType

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionUpdater:
    def __init__(self, option_picker: "OptionPicker"):
        self.option_picker = option_picker
        self.scroll_area = option_picker.option_scroll
        self.json_loader = option_picker.main_widget.json_manager.loader_saver

        # Automatically determine the app root directory
        self.app_root = self._get_app_root()
        self.profiler = self.option_picker.main_widget.main_window.profiler

    def _get_app_root(self) -> str:
        """Determine the root path of the application."""
        # Get the directory of the current file
        current_file_path = os.path.abspath(__file__)
        # Traverse up to the root of the project (adjust levels if needed)
        return os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

    def refresh_options(self):
        # @self.profiler.profile
        def _refresh_options():
            sequence = self.json_loader.load_current_sequence_json()
            if len(sequence) > 1:
                sections = self.scroll_area.sections
                pictograph_frames = []
                for section in sections.values():
                    pictograph_frames.append(section.pictograph_frame)

                self.option_picker.main_widget.fade_manager.widget_fader.fade_and_update(
                    pictograph_frames, self.update_options, 200
                )

        _refresh_options()


    def update_options(self):
        # @self.profiler.profile
        def _update_options():
            sequence = self.json_loader.load_current_sequence_json()
            selected_filter = (
                self.option_picker.reversal_filter.reversal_combobox.currentData()
            )
            next_options = self.option_picker.option_getter.get_next_options(
                sequence, selected_filter
            )

            for section in self.option_picker.option_scroll.sections.values():
                section.clear_pictographs()

            for i, pictograph_dict in enumerate(next_options):
                pictograph = self.option_picker.option_pool[i]
                pictograph.updater.update_pictograph(pictograph_dict)
                pictograph.view.update_borders()
                self.scroll_area.sections[
                    LetterType.get_letter_type(pictograph.letter)
                ].add_pictograph(pictograph)
        self.profiler.enable()

        _update_options()
        self.profiler.disable()
        self.profiler.write_profiling_stats_to_file(
            "option_updater_profile.txt", os.getcwd()
        )