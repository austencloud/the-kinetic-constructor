from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexRotationManager:
    """Handles rotating the Codex pictographs in 45° increments."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        self.rotation_steps = 0
        self.loc_order = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

    def rotate_codex(self):
        """Rotate all pictographs in the Codex by 45° increments."""
        if not self.codex.data_manager.pictograph_data:
            return

        self.rotation_steps = 1
        for letter, pictograph in self.codex.data_manager.pictograph_data.items():
            if pictograph:
                dict = self._rotate_pictograph(pictograph)
                self.codex.data_manager.pictograph_data[letter] = dict
        for view in self.codex.section_manager.views.values():
            view.pictograph.grid.update_grid_mode()
        self._refresh_pictograph_views()

    def _rotate_pictograph(self, pictograph_dict: dict) -> dict:
        """Rotate a single pictograph dictionary."""
        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_dict:
                attributes = pictograph_dict[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"], self.rotation_steps
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(
                        attributes["end_loc"], self.rotation_steps
                    )

        if "blue_attributes" in pictograph_dict and "red_attributes" in pictograph_dict:
            bl = pictograph_dict["blue_attributes"]
            rl = pictograph_dict["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                pictograph_dict["start_pos"] = self.get_position_name(
                    bl["start_loc"], rl["start_loc"]
                )
            if "end_loc" in bl and "end_loc" in rl:
                pictograph_dict["end_pos"] = self.get_position_name(
                    bl["end_loc"], rl["end_loc"]
                )
        return pictograph_dict

    def _rotate_location(self, location: str, rotation_steps: int) -> str:
        """Rotate a single location by 45° increments."""
        if location not in self.loc_order:
            return location
        idx = self.loc_order.index(location)
        new_idx = (idx + rotation_steps) % len(self.loc_order)
        new_loc = self.loc_order[new_idx]
        return new_loc

    def get_position_name(self, left_loc: str, right_loc: str) -> str:
        """Retrieve position name from a map based on left and right locations."""
        try:
            from data.positions_map import positions_map

            return positions_map[(left_loc, right_loc)]
        except KeyError:
            return "unknown"  # Handle missing mappings gracefully

    def update_grid_mode(self):
        for view in self.codex.section_manager.views.values():
            grid_mode = self.codex.main_widget.grid_mode_checker.get_grid_mode(
                view.pictograph.pictograph_dict
            )
            view.pictograph.grid.hide()
            view.pictograph.grid.__init__(
                view.pictograph, view.pictograph.grid.grid_data, grid_mode
            )

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_dict = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.arrow_placement_manager.default_positioner.__init__(
                    view.pictograph.arrow_placement_manager
                )
                view.pictograph.updater.update_pictograph(pictograph_dict)
