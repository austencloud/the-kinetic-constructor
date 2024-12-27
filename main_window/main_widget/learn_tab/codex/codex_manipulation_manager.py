# codex_modification_manager.py

from typing import TYPE_CHECKING
import logging

from main_window.main_widget.learn_tab.codex_widget.codex_color_swap_manager import (
    CodexColorSwapManager,
)
from main_window.main_widget.learn_tab.codex_widget.codex_mirror_manager import (
    CodexMirrorManager,
)
from main_window.main_widget.learn_tab.codex_widget.codex_rotation_manager import (
    CodexRotationManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex_widget.codex import Codex

logger = logging.getLogger(__name__)


class CodexManipulationManager:
    """Manages global modifications for the CodexWidget."""

    def __init__(self, codex: "Codex"):
        self.codex = codex

        self.mirror_manager = CodexMirrorManager(self)
        self.color_swap_manager = CodexColorSwapManager(self)
        self.rotation_manager = CodexRotationManager(self)

    def setup_connections(self):
        logger.debug("Setting up connections for global modifications.")
        # Accessing buttons from the parent's control_widget
        # self.codex.control_widget.rotate_btn.clicked.connect(self.rotate_all)
        self.codex.control_widget.mirror_btn.clicked.connect(self.mirror_all)
        self.codex.control_widget.color_swap_btn.clicked.connect(self.color_swap_all)
        self.codex.control_widget.orientation_selector.currentTextChanged.connect(
            self.update_orientation_all
        )

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

    def color_swap_all(self):
        logger.info("Color Swap action triggered.")
        try:
            for letter_str, view in self.codex.section_manager.pictograph_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    # Implement actual color swap logic here
                    scene.updater.update_pictograph(scene.pictograph_dict)
                    logger.debug(f"Swapped colors for pictograph '{letter_str}'.")
        except Exception as e:
            logger.exception(f"Error during color_swap_all: {e}")

    def update_orientation_all(self, orientation: str):
        logger.info(f"Orientation update triggered to '{orientation}'.")
        try:
            for letter_str, view in self.codex.section_manager.pictograph_views.items():
                scene = view.pictograph
                if scene.pictograph_dict:
                    new_dict = scene.pictograph_dict.copy()
                    if "blue_attributes" in new_dict:
                        new_dict["blue_attributes"]["start_ori"] = orientation
                    if "red_attributes" in new_dict:
                        new_dict["red_attributes"]["start_ori"] = orientation
                    scene.updater.update_pictograph(new_dict)
                    logger.debug(
                        f"Updated orientation for pictograph '{letter_str}' to '{orientation}'."
                    )
        except Exception as e:
            logger.exception(f"Error during update_orientation_all: {e}")
