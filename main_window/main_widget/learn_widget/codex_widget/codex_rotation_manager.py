from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex


class CodexRotationManager:
    """Handles rotating the Codex pictographs in 45° increments."""

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.rotation_steps = 0
        self.loc_order = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

    def rotate_codex(self):
        """Rotate all pictographs in the Codex by 45° increments."""
        if not self.codex.pictograph_data:
            return

        self.rotation_steps = 1
        for letter, pictograph in self.codex.pictograph_data.items():
            if pictograph:
                dict = self._rotate_pictograph(pictograph)
                self.codex.pictograph_data[letter] = dict
        # Update UI or grid modes if needed
        self.update_grid_mode()
        self.codex.section_manager.reload_sections()
        print("Codex rotated!")  # Replace with a UI message if required
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
        """Update grid mode for the Codex based on the final orientations of pictographs."""
        cardinal_set = {"n", "e", "s", "w"}
        intercardinal_set = {"ne", "se", "sw", "nw"}
        all_locs = []

        for pictograph_dict in self.codex.pictograph_data.values():
            if not pictograph_dict:
                continue
            if (
                "blue_attributes" in pictograph_dict
                and "red_attributes" in pictograph_dict
            ):
                bl = pictograph_dict["blue_attributes"].get("end_loc")
                rl = pictograph_dict["red_attributes"].get("end_loc")
                if bl:
                    all_locs.append(bl)
                if rl:
                    all_locs.append(rl)

        if all(l in cardinal_set for l in all_locs):
            mode = "diamond"
        elif all(l in intercardinal_set for l in all_locs):
            mode = "box"

        else:
            cardinal_count = sum(l in cardinal_set for l in all_locs)
            inter_count = sum(l in intercardinal_set for l in all_locs)
            mode = "diamond" if cardinal_count >= inter_count else "box"
        for view in self.codex.section_manager.pictograph_views.values():
            view.pictograph.grid.hide()
            view.pictograph.grid.__init__(
                view.pictograph, view.pictograph.grid.grid_data, mode
            )
        self.codex.main_widget.special_placement_loader.refresh_placements(mode)

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.pictograph_views.items():
            if letter in self.codex.pictograph_data:
                pictograph_dict = self.codex.pictograph_data[letter]
                grid_mode = self.codex.main_widget.grid_mode_checker.get_grid_mode(
                    pictograph_dict
                )
                view.pictograph.arrow_placement_manager.default_positioner.__init__(
                    view.pictograph.arrow_placement_manager, grid_mode
                )

                view.pictograph.updater.update_pictograph(pictograph_dict)
                view.pictograph.updater.update_motions(pictograph_dict)
                view.scene().update()
