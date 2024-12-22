from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex
    from main_window.main_widget.learn_widget.codex_widget.codex_manipulation_manager import CodexManipulationManager
    from main_window.main_widget.learn_widget.codex_widget.codex_color_swap_manager import CodexColorSwapManager

class CodexColorSwapManager:
    def __init__(self, manip_manager: "CodexManipulationManager"):
        self.codex = manip_manager.codex

    def swap_colors_in_codex(self):
        for pictograph in self.codex.pictograph_data.values():
            self._swap_colors(pictograph)

    def _swap_colors(self, pictograph):
        if not pictograph:
            return
        pictograph["blue_attributes"], pictograph["red_attributes"] = (
            pictograph["red_attributes"],
            pictograph["blue_attributes"],
        )
