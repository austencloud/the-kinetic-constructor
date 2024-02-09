from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
import pandas as pd
from constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from widgets.pictograph.pictograph import Pictograph
from widgets.sequence_builder.components.sequence_builder_letter_button_frame import (
    SequenceBuilderLetterButtonFrame,
)

from widgets.sequence_builder.components.sequence_builder_section_manager import (
    SequenceBuilderScrollAreaSectionsManager,
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
        self.current_pictograph: Pictograph = (
            None  # Store the last pictograph in the sequence
        )
        self.df = pd.read_csv("PictographDataframe.csv")  # Load the dataframe
        self.sections_manager_loaded = False
        self._setup_components()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout.addWidget(self.scroll_area, 5)
        self.right_layout.addWidget(self.letter_button_frame, 1)
        self.layout.addLayout(self.left_layout, 5)
        self.layout.addLayout(self.right_layout, 1)

    # Assuming Pictograph class has methods or attributes like end_red_ori and end_blue_ori
    def update_current_pictograph(self, pictograph: Pictograph):
        self.current_pictograph = pictograph
        self.current_end_red_ori = pictograph.red_motion.end_ori
        self.current_end_blue_ori = pictograph.blue_motion.end_ori
        self.get_next_options(pictograph.end_pos)

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
        self.scroll_area = SequenceBuilderScrollArea(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self.scroll_area)
        self.start_position_handler = StartPositionHandler(self)
        self.letter_button_frame = SequenceBuilderLetterButtonFrame(self)



    def transition_to_sequence_building(self, start_pictograph: Pictograph):
        # Hide start positions and show letter button frame in the correct layout
        self.start_position_handler.hide_start_positions()
        self.layout.addWidget(self.letter_button_frame)  # Add button frame to the main layout
        self.scroll_area.initialize_with_options()  # Initialize scroll area with the available options

        self.update_current_pictograph(start_pictograph)
        self.scroll_area.show()

    def render_and_store_pictograph(self, pictograph_data: pd.Series):
        pictograph_key = f"{pictograph_data['letter']}_{pictograph_data['start_pos']}→{pictograph_data['end_pos']}"
        pictograph_dict = pictograph_data.to_dict()

        # Adjust the dict with the correct orientations
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
        self.scroll_area.resize_sequence_builder_scroll_area()
        self.letter_button_frame.resize_sequence_builder_letter_button_frame()
