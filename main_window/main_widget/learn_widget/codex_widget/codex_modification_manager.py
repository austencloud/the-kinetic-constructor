# codex_modification_manager.py

from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex

logger = logging.getLogger(__name__)


class CodexModificationManager:
    """Manages global modifications for the CodexWidget."""

    def __init__(self, parent: "Codex"):
        self.parent = parent
        self.setup_connections()

    def setup_connections(self):
        logger.debug("Setting up connections for global modifications.")
        self.parent.rotate_btn.clicked.connect(self.rotate_all)
        self.parent.mirror_btn.clicked.connect(self.mirror_all)
        self.parent.color_swap_btn.clicked.connect(self.color_swap_all)
        self.parent.orientation_selector.currentTextChanged.connect(
            self.update_orientation_all
        )

    def rotate_all(self):
        logger.info("Rotate action triggered.")
        try:
            sequence_rotation_manager = self.parent.main_widget.sequence_widget.rotation_manager
            for letter_str, view in self.parent.section_manager.letter_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    rotated_pictograph_dict = scene.pictograph_dict.copy()
                    sequence_rotation_manager.rotate_pictograph(rotated_pictograph_dict, 1)
                    scene.updater.update_pictograph(rotated_pictograph_dict)
                    logger.debug(f"Rotated pictograph for letter '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during rotate_all: {e}")

    def mirror_all(self):
        logger.info("Mirror action triggered.")
        try:
            for letter_str, view in self.parent.section_manager.letter_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    # Implement actual mirror logic here
                    # Placeholder: just re-update the same dict
                    scene.updater.update_pictograph(scene.pictograph_dict)
                    logger.debug(f"Mirrored pictograph for letter '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during mirror_all: {e}")

    def color_swap_all(self):
        logger.info("Color Swap action triggered.")
        try:
            for letter_str, view in self.parent.section_manager.letter_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    # Implement actual color swap logic here
                    # Placeholder: just re-update the same dict
                    scene.updater.update_pictograph(scene.pictograph_dict)
                    logger.debug(f"Swapped colors for pictograph '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during color_swap_all: {e}")

    def update_orientation_all(self, orientation: str):
        logger.info(f"Orientation update triggered to '{orientation}'.")
        try:
            for letter_str, view in self.parent.section_manager.letter_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    new_dict = scene.pictograph_dict.copy()
                    if "blue_attributes" in new_dict:
                        new_dict["blue_attributes"]["start_ori"] = orientation
                    if "red_attributes" in new_dict:
                        new_dict["red_attributes"]["start_ori"] = orientation
                    scene.updater.update_pictograph(new_dict)
                    logger.debug(f"Updated orientation for pictograph '{letter_str}' to '{orientation}'.")
        except Exception as e:
            logger.exception(f"Error during update_orientation_all: {e}")
