from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from contextlib import contextmanager
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BOX, DIAMOND
from copy import deepcopy

if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.manual_builder import (
        ManualBuilderWidget,
    )


class BaseStartPosPicker(QWidget):
    def __init__(self, manual_builder: "ManualBuilderWidget"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.pictograph_cache: dict[str, BasePictograph] = {}
        self.box_pictographs: list[BasePictograph] = []
        self.diamond_pictographs: list[BasePictograph] = []

    @contextmanager
    def temporary_grid_mode(self, grid_mode):
        """Context manager to temporarily set the grid mode."""
        original_mode = (
            self.main_widget.settings_manager.global_settings.get_grid_mode()
        )
        self.main_widget.settings_manager.global_settings.set_grid_mode(grid_mode)
        yield
        self.main_widget.settings_manager.global_settings.set_grid_mode(original_mode)

    def create_pictograph_from_dict(
        self, pictograph_dict: dict, target_grid_mode
    ) -> BasePictograph:
        """Create a pictograph under the specified grid mode, using cache if available."""
        pictograph_key = self.generate_pictograph_key(pictograph_dict, target_grid_mode)
        if pictograph_key in self.pictograph_cache:
            return self.pictograph_cache[pictograph_key]

        with self.temporary_grid_mode(target_grid_mode):
            pictograph = BasePictograph(self.main_widget)
            pictograph.updater.update_pictograph(deepcopy(pictograph_dict))
            self.pictograph_cache[pictograph_key] = pictograph

            # Append to the list based on the grid mode
            if target_grid_mode == BOX:
                self.box_pictographs.append(pictograph)
            elif target_grid_mode == DIAMOND:
                self.diamond_pictographs.append(pictograph)

        return pictograph

    def generate_pictograph_key(self, pictograph_dict, grid_mode):
        """Generate a unique key for the pictograph based on its attributes and grid mode."""
        letter = pictograph_dict["letter"]
        start_pos = pictograph_dict["start_pos"]
        end_pos = pictograph_dict["end_pos"]
        return f"{letter}_{start_pos}_{end_pos}_{grid_mode}"

    def get_box_variations(self) -> list[BasePictograph]:
        """Retrieve box mode variations."""
        if self.box_pictographs:
            return self.box_pictographs  # Return cached variations

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
        for letter in self.main_widget.pictograph_dicts:
            for pictograph_dict in self.main_widget.pictograph_dicts[letter]:
                if pictograph_dict["start_pos"] == pictograph_dict["end_pos"]:
                    if pictograph_dict["start_pos"] in box_positions:
                        self.create_pictograph_from_dict(pictograph_dict, BOX)
        return self.box_pictographs

    def get_diamond_variations(self) -> list[BasePictograph]:
        """Retrieve diamond mode variations."""
        if self.diamond_pictographs:
            return self.diamond_pictographs  # Return cached variations

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
        for letter in self.main_widget.pictograph_dicts:
            for pictograph_dict in self.main_widget.pictograph_dicts[letter]:
                if pictograph_dict["start_pos"] == pictograph_dict["end_pos"]:
                    if pictograph_dict["start_pos"] in diamond_positions:
                        self.create_pictograph_from_dict(pictograph_dict, DIAMOND)
        return self.diamond_pictographs
