import logging
from typing import TYPE_CHECKING


logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex.codex_control_widget import (
        CodexControlWidget,
    )


class CodexMirrorManager:
    """Handles mirroring of pictographs in the Codex."""

    def __init__(self, control_widget: "CodexControlWidget"):
        self.codex = control_widget.codex
        # Define mappings for mirroring positions and locations
        self.vertical_mirror_positions = {
            "alpha1": "alpha1",
            "alpha2": "alpha8",
            "alpha3": "alpha7",
            "alpha4": "alpha6",
            "alpha5": "alpha5",
            "alpha6": "alpha4",
            "alpha7": "alpha3",
            "alpha8": "alpha2",
            "beta1": "beta1",
            "beta2": "beta8",
            "beta3": "beta7",
            "beta4": "beta6",
            "beta5": "beta5",
            "beta6": "beta4",
            "beta7": "beta3",
            "beta8": "beta2",
            "gamma1": "gamma9",
            "gamma2": "gamma16",
            "gamma3": "gamma15",
            "gamma4": "gamma14",
            "gamma5": "gamma13",
            "gamma6": "gamma12",
            "gamma7": "gamma11",
            "gamma8": "gamma10",
            "gamma9": "gamma1",
            "gamma10": "gamma8",
            "gamma11": "gamma7",
            "gamma12": "gamma6",
            "gamma13": "gamma5",
            "gamma14": "gamma4",
            "gamma15": "gamma3",
            "gamma16": "gamma2",
        }

        self.vertical_mirror_locations = {
            "n": "n",
            "e": "w",
            "w": "e",
            "s": "s",
            "ne": "nw",
            "nw": "ne",
            "se": "sw",
            "sw": "se",
        }

    def mirror_all(self):
        logger.info("Mirror action triggered.")
        try:
            for letter_str, view in self.codex.section_manager.pictograph_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    # Implement actual mirror logic here
                    scene.updater.update_pictograph(scene.pictograph_dict)
                    logger.debug(f"Mirrored pictograph for letter '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during mirror_all: {e}")

    def mirror_codex(self):
        """Apply mirroring logic to all pictographs in the Codex."""
        for letter, pictograph in self.codex.data_manager.pictograph_data.items():
            if pictograph:
                self._mirror_pictograph(pictograph)
        self._refresh_pictograph_views()

    def _mirror_pictograph(self, pictograph):
        """Mirror an individual pictograph dictionary."""
        if "start_pos" in pictograph:
            pictograph["start_pos"] = self.vertical_mirror_positions.get(
                pictograph["start_pos"], pictograph["start_pos"]
            )
        if "end_pos" in pictograph:
            pictograph["end_pos"] = self.vertical_mirror_positions.get(
                pictograph["end_pos"], pictograph["end_pos"]
            )

        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph:
                attributes = pictograph[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self.vertical_mirror_locations.get(
                        attributes["start_loc"], attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self.vertical_mirror_locations.get(
                        attributes["end_loc"], attributes["end_loc"]
                    )
                if "prop_rot_dir" in attributes:
                    attributes["prop_rot_dir"] = self._reverse_prop_rot_dir(
                        attributes["prop_rot_dir"]
                    )

    def _reverse_prop_rot_dir(self, prop_rot_dir):
        """Reverse the rotation direction."""
        return {"cw": "ccw", "ccw": "cw"}.get(prop_rot_dir, prop_rot_dir)

    def _refresh_pictograph_views(self):
        """Refresh all views to reflect the updated pictograph data."""
        for letter, view in self.codex.section_manager.pictograph_views.items():
            if letter in self.codex.data_manager.pictograph_data:
                pictograph_dict = self.codex.data_manager.pictograph_data[letter]
                view.pictograph.updater.update_pictograph(pictograph_dict)
                view.scene().update()
