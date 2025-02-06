from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING
from Enums.letters import Letter
from data.constants import BOX, DIAMOND, START_POS, END_POS
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from ...sequence_widget.beat_frame.start_pos_beat import StartPositionBeat
from .start_pos_picker_variations_button import StartPosVariationsButton
from .start_pos_pictograph_frame import StartPosPickerPictographFrame
from .choose_your_start_pos_label import ChooseYourStartPosLabel
from .base_start_pos_picker import BaseStartPosPicker

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab


class StartPosPicker(BaseStartPosPicker):
    SPACING = 10
    start_position_selected = pyqtSignal(BasePictograph)
    COLUMN_COUNT = 3

    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.button_layout = self._setup_variations_button_layout()
        self.setup_layout()
        self.setObjectName("StartPosPicker")
        self.setStyleSheet("background-color: white;")
        self.initialized = False
        self.start_options: dict[str, BasePictograph] = {}

        self.display_variations()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.start_label_layout = QHBoxLayout()
        self.pictograph_layout = QHBoxLayout()

        self.start_label_layout.addWidget(self.choose_your_start_pos_label)
        self.pictograph_layout.addWidget(self.pictograph_frame)

        self.layout.addStretch(1)
        self.layout.addLayout(self.start_label_layout, 1)
        self.layout.addStretch(1)
        self.layout.addLayout(self.pictograph_layout, 5)
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_layout, 5)
        self.layout.addStretch(1)

    def _setup_variations_button_layout(self) -> QHBoxLayout:
        self.variations_button = StartPosVariationsButton(self)
        self.variations_button.clicked.connect(
            self.construct_tab.transition_to_advanced_start_pos_picker
        )
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.variations_button)
        button_layout.addStretch(1)
        return button_layout

    def display_variations(self) -> None:
        """Load only the start positions relevant to the current grid mode."""
        self.pictograph_frame.clear_pictographs()
        grid_mode = DIAMOND
        start_pos_keys = (
            ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
            if grid_mode == DIAMOND
            else ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]
        )
        if grid_mode == BOX:
            self.get_box_pictographs()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(position_key, BOX)
        elif grid_mode == DIAMOND:
            self.get_diamond_pictographs()
            for position_key in start_pos_keys:
                self._add_start_position_option_to_start_pos_frame(
                    position_key, DIAMOND
                )

    def _add_start_position_option_to_start_pos_frame(
        self, position_key: str, grid_mode: str
    ) -> None:
        """Adds an option for the specified start position based on the current grid mode."""
        self.start_position_adder = (
            self.construct_tab.main_widget.sequence_widget.beat_frame.start_position_adder
        )
        start_pos, end_pos = position_key.split("_")
        for letter, pictograph_dicts in self.main_widget.pictograph_dicts.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    pictograph = self.create_pictograph_from_dict(
                        pictograph_dict, grid_mode
                    )
                    self.start_options[letter] = pictograph
                    pictograph.letter = letter
                    pictograph.start_pos = start_pos
                    pictograph.end_pos = end_pos
                    self.pictograph_frame._add_start_pos_to_layout(pictograph)

                    pictograph.start_to_end_pos_glyph.hide()
                    break

    def convert_current_sequence_json_entry_to_start_pos_pictograph(
        self, start_pos_entry
    ) -> StartPositionBeat:
        start_position_pictograph = self.get_start_pos_pictograph(
            start_pos_entry[1] if start_pos_entry else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget.sequence_widget.beat_frame,
        )
        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_dict
        )

        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "BasePictograph":
        if not start_pos_data:
            return None
        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.pictograph_dicts.get(letter, [])
        for pictograph_dict in matching_letter_pictographs:
            if pictograph_dict["start_pos"] == start_pos_key:

                pictograph_dict["blue_attributes"]["start_ori"] = start_pos_data[
                    "blue_attributes"
                ]["end_ori"]
                pictograph_dict["red_attributes"]["start_ori"] = start_pos_data[
                    "red_attributes"
                ]["end_ori"]
                pictograph_factory = (
                    self.main_widget.sequence_widget.beat_frame.beat_factory
                )
                pictograph_key = (
                    self.main_widget.pictograph_key_generator.generate_pictograph_key(
                        pictograph_dict
                    )
                )
                start_pos_pictograph = pictograph_factory.create_start_pos_beat(
                    pictograph_key, pictograph_dict
                )
                return start_pos_pictograph

        print(f"No matching start position found for key: {start_pos_key}")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str) -> str:
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None
