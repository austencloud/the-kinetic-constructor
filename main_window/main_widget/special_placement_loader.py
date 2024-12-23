import json
import os
from typing import TYPE_CHECKING
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SpecialPlacementLoader:
    """
    A loader that pulls special placement data for *all* supported grid modes at once.
    Each pictograph can then pick the correct offsets from self.special_placements[their_mode].
    """

    # Subfolders used in arrow_placement/...
    SUBFOLDERS = [
        "from_layer1",
        "from_layer2",
        "from_layer3_blue2_red1",
        "from_layer3_blue1_red2",
    ]

    # Example: we currently support "diamond" and "box" as grid modes
    SUPPORTED_MODES = ["diamond", "box"]

    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

        # A nested dict structure for all modes, e.g.:
        # {
        #   "diamond": {
        #       "from_layer1": {...},
        #       "from_layer2": {...},
        #       ...
        #   },
        #   "box": {
        #       "from_layer1": {...},
        #       "from_layer2": {...},
        #       ...
        #   }
        # }
        self.special_placements: dict[str, dict[str, dict]] = {}

        # Load everything up front
        self.load_all_modes()

    def load_all_modes(self) -> None:
        """
        Loads special placement data for each mode in SUPPORTED_MODES.
        Stores the result in self.special_placements[mode].
        """
        for mode in self.SUPPORTED_MODES:
            self.special_placements[mode] = self._load_mode_subfolders(mode)

        # Optionally, you could store the loaded structure
        # in main_widget.special_placements if needed:
        self.main_widget.special_placements = self.special_placements

    def _load_mode_subfolders(self, mode: str) -> dict[str, dict]:
        """
        Loads data for each subfolder (from_layer1, from_layer2, etc.)
        under arrow_placement/<mode>/special/<subfolder>.
        Returns a dict like:
        {
          "from_layer1": { ...all JSON data merged... },
          "from_layer2": { ... },
          ...
        }
        """
        mode_data: dict[str, dict] = {}
        for subfolder in self.SUBFOLDERS:
            mode_data[subfolder] = {}
            directory = get_images_and_data_path(
                f"data/arrow_placement/{mode}/special/{subfolder}"
            )
            # Iterate over JSON files
            if not os.path.isdir(directory):
                # It's valid to handle missing directories as needed
                continue
            for file_name in os.listdir(directory):
                if file_name.endswith("_placements.json"):
                    path = os.path.join(directory, file_name)
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Merge into the existing dict
                        mode_data[subfolder].update(data)
        return mode_data

    def get_placements_for_mode(self, grid_mode: str) -> dict:
        """
        Returns the entire nested dict for a particular grid_mode.
        Example: self.special_placements["diamond"] or self.special_placements["box"].
        """
        return self.special_placements.get(grid_mode, {})

    # def refresh_for_pictograph_mode(self, grid_mode: str) -> None:
    #     """
    #     An example method that updates *only* pictographs that explicitly have `pictograph_dict["grid_mode"] == grid_mode`.
    #     This no longer depends on the global setting.
    #     """
    #     # Make sure we have data for that mode. If not, do nothing or load it.
    #     if grid_mode not in self.special_placements:
    #         return  # or optionally load it on-demand

    #     # Then update only the pictographs in that mode
    #     for letter_dict in self.main_widget.pictograph_cache.values():
    #         for pictograph in letter_dict.values():
    #             # We assume each pictograph has .pictograph_dict['grid_mode'] set
    #             if pictograph.pictograph_dict.get("grid_mode") == grid_mode:
    #                 pictograph.updater.update_pictograph()
    #                 pictograph.update()
