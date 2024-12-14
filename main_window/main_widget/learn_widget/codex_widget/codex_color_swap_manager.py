from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex


class CodexColorSwapManager:
    def __init__(self, codex: "Codex"):
        self.codex = codex

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
