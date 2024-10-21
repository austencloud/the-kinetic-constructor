import json
from typing import TYPE_CHECKING

from Enums.PropTypes import PropType
from Enums.letters import Letter
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
from styles.main_widget_tab_bar_styler import MainWidgetTabBarStyler

if TYPE_CHECKING:
    from .main_widget import MainWidget
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


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
        self._setup_special_placements()

    def _initialize_managers(self):
        """Setup all the managers and helper components."""
        self.splash_screen.update_progress(20, "Loading JSON Manager...")
        self.main_widget.json_manager = JsonManager(self.main_widget)

        self.splash_screen.update_progress(30, "Loading SVG Manager...")
        self.main_widget.svg_manager = SvgManager(self.main_widget)

        self.splash_screen.update_progress(40, "Loading key generators...")
        self.main_widget.turns_tuple_generator = TurnsTupleGenerator()
        self.main_widget.pictograph_key_generator = PictographKeyGenerator(
            self.main_widget
        )

        self.splash_screen.update_progress(50, "Loading special placements...")
        self.main_widget.special_placement_loader = SpecialPlacementLoader(
            self.main_widget
        )

        self.splash_screen.update_progress(60, "Loading Metadata Extractor...")
        self.main_widget.metadata_extractor = MetaDataExtractor(self.main_widget)
        self.main_widget.tab_bar_styler = MainWidgetTabBarStyler(self.main_widget)
        self.main_widget.sequence_level_evaluator = SequenceLevelEvaluator()
        self.main_widget.sequence_properties_manager = SequencePropertiesManager(
            self.main_widget
        )
        self.main_widget.thumbnail_finder = ThumbnailFinder(self.main_widget)
        self.main_widget.grid_mode_checker = GridModeChecker()

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

    def _setup_special_placements(self) -> None:
        self.main_widget.special_placements = (
            self.main_widget.special_placement_loader.load_special_placements()
        )

    def _setup_letters(self) -> None:
        self.splash_screen.update_progress(10, "Loading pictograph dictionaries...")
        self.main_widget.pictograph_dict_loader = PictographDictLoader(self.main_widget)
        self.main_widget.pictograph_dicts = (
            self.main_widget.pictograph_dict_loader.load_all_pictograph_dicts()
        )
        self.main_widget.letter_determiner = LetterDeterminer(self.main_widget)

    def set_grid_mode(self, grid_mode: str) -> None:
            self.main_window.settings_manager.global_settings.set_grid_mode(grid_mode)

            self.main_window.settings_manager.save_settings()
            self.main_widget.special_placement_loader.refresh_placements()
            self.pictograph_dicts = self.main_widget.pictograph_dict_loader.load_all_pictograph_dicts()

            start_pos_manager = (
                self.main_widget.manual_builder.start_pos_picker.start_pos_manager
            )
            start_pos_manager.clear_start_positions()
            start_pos_manager.setup_start_positions()

            sequence_clearer = self.main_widget.sequence_widget.sequence_clearer
            sequence_clearer.clear_sequence(show_indicator=False)

            pictograph_container = (
                self.main_widget.sequence_widget.graph_editor.pictograph_container
            )

            pictograph_container.GE_pictograph_view.set_to_blank_grid()
            self._setup_special_placements()