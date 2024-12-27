import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from Enums.PropTypes import PropType
from data.constants import IN
from letter_determiner.letter_determiner import LetterDeterminer
from utilities.path_helpers import get_images_and_data_path

from .grid_mode_checker import GridModeChecker
from .pcitograph_dict_loader import PictographDictLoader
from .sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from .sequence_level_evaluator import SequenceLevelEvaluator
from .thumbnail_finder import ThumbnailFinder
from .metadata_extractor import MetaDataExtractor
from .json_manager.json_manager import JsonManager
from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from .pictograph_key_generator import PictographKeyGenerator
from .special_placement_loader import SpecialPlacementLoader
from objects.graphical_object.svg_manager.graphical_object_svg_manager import SvgManager

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetManager:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.splash_screen = main_widget.splash_screen
        self.settings_manager = main_widget.settings_manager
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._initialize_managers()
        self._setup_letters()

    def _initialize_managers(self):
        """Setup all the managers and helper components."""
        mw = self.main_widget
        mw.json_manager = JsonManager(mw)
        mw.svg_manager = SvgManager(mw)
        mw.turns_tuple_generator = TurnsTupleGenerator()
        mw.pictograph_key_generator = PictographKeyGenerator(mw)
        mw.special_placement_loader = SpecialPlacementLoader(mw)
        mw.metadata_extractor = MetaDataExtractor(mw)
        mw.sequence_level_evaluator = SequenceLevelEvaluator()
        mw.sequence_properties_manager = SequencePropertiesManager(mw)
        mw.thumbnail_finder = ThumbnailFinder(mw)
        mw.grid_mode_checker = GridModeChecker()

    def _setup_pictograph_cache(self) -> None:
        from Enums.Enums import Letter

        self.main_widget.pictograph_cache = {}
        for letter in Letter:
            self.main_widget.pictograph_cache[letter] = {}

    def _set_prop_type(self) -> None:
        settings_path = get_images_and_data_path("settings.json")
        with open(settings_path, "r", encoding="utf-8") as file:
            settings: dict[str, dict[str, str | bool]] = json.load(file)
        prop_type_value = settings.get("global", {}).get("prop_type", "staff")
        self.main_widget.prop_type = PropType.get_prop_type(prop_type_value)

    def _setup_letters(self) -> None:
        self.main_widget.pictograph_dict_loader = PictographDictLoader(self.main_widget)
        self.main_widget.pictograph_dicts = (
            self.main_widget.pictograph_dict_loader.load_all_pictograph_dicts()
        )
        self.main_widget.letter_determiner = LetterDeterminer(self.main_widget)

    def set_grid_mode(self, grid_mode: str, clear_sequence=True) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.main_window.settings_manager.global_settings.set_grid_mode(grid_mode)
        self.pictograph_dicts = (
            self.main_widget.pictograph_dict_loader.load_all_pictograph_dicts()
        )

        start_pos_picker = self.main_widget.constructor_tab.start_pos_picker
        start_pos_picker.display_variations(grid_mode)
        advanced_start_pos_picker = (
            self.main_widget.constructor_tab.advanced_start_pos_picker
        )
        advanced_start_pos_picker.display_variations(grid_mode)

        sequence_clearer = self.main_widget.sequence_widget.sequence_clearer
        if (
            self.main_widget.constructor_tab.stacked_widget.currentWidget()
            == self.main_widget.constructor_tab.advanced_start_pos_picker
        ):
            should_reset_to_start_pos_picker = False
        else:
            should_reset_to_start_pos_picker = True
        if clear_sequence:
            sequence_clearer.clear_sequence(
                show_indicator=False,
                should_reset_to_start_pos_picker=should_reset_to_start_pos_picker,
            )
            adjustment_panel = (
                self.main_widget.sequence_widget.graph_editor.adjustment_panel
            )
            for picker in [
                adjustment_panel.blue_ori_picker,
                adjustment_panel.red_ori_picker,
            ]:
                picker.ori_picker_widget.ori_setter.set_orientation(IN)
            pictograph_container = (
                self.main_widget.sequence_widget.graph_editor.pictograph_container
            )
            pictograph_container.GE_pictograph_view.set_to_blank_grid()
        option_picker = self.main_widget.constructor_tab.option_picker
        for pictograph in option_picker.option_pool:
            pictograph.grid.hide()
            pictograph.grid.__init__(pictograph, pictograph.grid.grid_data, grid_mode)

        beat_frame = self.main_widget.sequence_widget.beat_frame
        for beat in beat_frame.beats:
            if beat.is_filled:
                beat.beat.grid.hide()
                beat.beat.grid.__init__(beat.beat, beat.beat.grid.grid_data, grid_mode)
        start_pos = beat_frame.start_pos_view.start_pos
        start_pos.grid.hide()
        start_pos.grid.__init__(start_pos, start_pos.grid.grid_data, grid_mode)
        QApplication.restoreOverrideCursor()
