from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from copy import deepcopy

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BOX, DIAMOND
from main_window.main_widget.sequence_builder.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.manual_builder import ManualBuilder


class BaseStartPosPicker(QWidget):
    def __init__(self, manual_builder: "ManualBuilder"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget

        # For caching pictographs based on letter, start_pos, end_pos, grid_mode
        self.pictograph_cache: dict[str, BasePictograph] = {}

        # Track the pictographs for each mode
        self.box_pictographs: list[BasePictograph] = []
        self.diamond_pictographs: list[BasePictograph] = []

    def create_pictograph_from_dict(
        self, pictograph_dict: dict, target_grid_mode: str, advanced: bool = False
    ) -> BasePictograph:
        """
        Create a pictograph using the provided dictionary, setting a local grid_mode.
        No context managers, no flipping global states.
        """
        # Make a local copy and inject 'grid_mode'
        local_dict = deepcopy(pictograph_dict)
        local_dict["grid_mode"] = target_grid_mode

        pictograph_key = self.generate_pictograph_key(local_dict, target_grid_mode)
        if pictograph_key in self.pictograph_cache:
            return self.pictograph_cache[pictograph_key]

        # Build the pictograph
        pictograph = BasePictograph(self.main_widget)
        pictograph.view = StartPosPickerPictographView(pictograph)
        pictograph.updater.update_pictograph(local_dict)
        pictograph.view.update_borders()

        # Cache it
        self.pictograph_cache[pictograph_key] = pictograph

        # Add to the appropriate list
        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)

        return pictograph

    def generate_pictograph_key(self, pictograph_dict: dict, grid_mode: str) -> str:
        """
        Generate a unique key based on letter, start_pos, end_pos, and grid_mode.
        """
        letter = pictograph_dict.get("letter", "unknown")
        start_pos = pictograph_dict.get("start_pos", "no_start")
        end_pos = pictograph_dict.get("end_pos", "no_end")
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def get_box_variations(self, advanced: bool = False) -> list[BasePictograph]:
        """
        Load pictographs for box mode. No context manager usage. We just
        call create_pictograph_from_dict(...) with 'BOX'.
        """
        if self.box_pictographs:
            return self.box_pictographs

        box_positions = [
            "alpha2",
            "alpha4",
            "alpha6",
            "alpha8",
            "beta2",
            "beta4",
            "beta6",
            "beta8",
            "gamma2",
            "gamma4",
            "gamma6",
            "gamma8",
            "gamma10",
            "gamma12",
            "gamma14",
            "gamma16",
        ]

        for letter, p_dicts in self.main_widget.pictograph_dicts.items():
            for p_dict in p_dicts:
                if p_dict["start_pos"] == p_dict["end_pos"]:
                    if p_dict["start_pos"] in box_positions:
                        # Just call create_pictograph_from_dict - no with-statement needed
                        self.create_pictograph_from_dict(p_dict, BOX)

        return self.box_pictographs

    def get_diamond_variations(self, advanced: bool = False) -> list[BasePictograph]:
        """
        Load pictographs for diamond mode. No context manager usage.
        """
        if self.diamond_pictographs:
            return self.diamond_pictographs

        diamond_positions = [
            "alpha1",
            "alpha3",
            "alpha5",
            "alpha7",
            "beta1",
            "beta3",
            "beta5",
            "beta7",
            "gamma1",
            "gamma3",
            "gamma5",
            "gamma7",
            "gamma9",
            "gamma11",
            "gamma13",
            "gamma15",
        ]

        for letter, p_dicts in self.main_widget.pictograph_dicts.items():
            for p_dict in p_dicts:
                if p_dict["start_pos"] == p_dict["end_pos"]:
                    if p_dict["start_pos"] in diamond_positions:
                        self.create_pictograph_from_dict(p_dict, DIAMOND)

        return self.diamond_pictographs
