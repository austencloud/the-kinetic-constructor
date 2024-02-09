from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
import pandas as pd
from constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from widgets.sequence_builder.components.option_picker import OptionPicker
from widgets.sequence_builder.components.start_position_picker import (
    StartPosPicker,
)
from ..pictograph.pictograph import Pictograph
from ..sequence_builder.components.sequence_builder_letter_button_frame import (
    OptionPickerLetterButtonFrame,
)

from .components.sequence_builder_scroll_area import SequenceBuilderScrollArea
from .components.clickable_option_handler import SequenceBuilderClickableOptionHandler
from .components.start_position_handler import StartPositionHandler
from ..scroll_area.components.sequence_builder_display_manager import (
    SequenceBuilderDisplayManager,
)
from ..scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.current_pictograph: Pictograph = None
        self.df = pd.read_csv("PictographDataframe.csv")  # Load the dataframe
        self.sections_manager_loaded = False
        self.selected_letters = None
        self._setup_components()

        self.start_position_picker = StartPosPicker(self)
        self.option_picker = OptionPicker(self)
        self.start_position_picker.position_selected.connect(
            self.on_start_position_selected
        )

    def update_current_pictograph(self, pictograph: Pictograph):
        self.current_pictograph = pictograph
        self.current_end_red_ori = pictograph.red_motion.end_ori
        self.current_end_blue_ori = pictograph.blue_motion.end_ori
        self.get_next_options(pictograph.end_pos)

    def on_start_position_selected(self, position: str):
        # Logic to initialize option_picker based on selected start position
        self.option_picker.scroll_area.initialize_with_options()

        options = self.get_next_options(position)
        self.option_picker.update_options(options)

    def get_next_options(self, end_pos):
        """Fetches and renders next options based on the end position."""
        matching_rows: pd.DataFrame = self.df[self.df["start_pos"] == end_pos]
        for _, row in matching_rows.iterrows():
            pictograph_key = f"{row['letter']}_{row['start_pos']}→{row['end_pos']}"
            if pictograph_key not in self.main_widget.all_pictographs:
                self.render_and_store_pictograph(row)

    def _setup_components(self):
        self.clickable_option_handler = SequenceBuilderClickableOptionHandler(self)
        self.display_manager = SequenceBuilderDisplayManager(self)

    def transition_to_sequence_building(self, start_pictograph: Pictograph):
        self.start_position_picker.hide_start_positions()
        self.update_current_pictograph(start_pictograph)
        self.start_position_picker.hide()
        self.option_picker.show()

    def render_and_store_pictograph(self, pictograph_data: pd.Series):
        pictograph_key = f"{pictograph_data['letter']}_{pictograph_data['start_pos']}→{pictograph_data['end_pos']}"
        pictograph_dict = pictograph_data.to_dict()

        pictograph_dict[RED_START_ORI] = self.current_end_red_ori
        pictograph_dict[BLUE_START_ORI] = self.current_end_blue_ori
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_TURNS] = 0

        new_pictograph = self.pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict
        )

        if pictograph_key not in self.main_widget.all_pictographs.get(
            pictograph_data["letter"], {}
        ):
            self.main_widget.all_pictographs[pictograph_data["letter"]][
                pictograph_key
            ] = new_pictograph

    def resize_sequence_builder(self) -> None:
        self.option_picker.scroll_area.resize_option_picker_scroll_area()
        self.option_picker.letter_button_frame.resize_option_picker_letter_button_frame()
