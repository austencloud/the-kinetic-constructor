# grid_mode_dialog.py
from typing import TYPE_CHECKING
from ..options_dialog import OptionsDialog

if TYPE_CHECKING:
    from .grid_mode_selector import GridModeSelector


class GridModeDialog:
    def __init__(self, grid_mode_selector: "GridModeSelector"):
        self.grid_mode_selector = grid_mode_selector
        self.options = ["Diamond", "Box"]

    def show_dialog(self):
        dialog = OptionsDialog(
            selector=self.grid_mode_selector,
            options=self.options,
            callback=self.option_selected,
        )
        dialog.show_dialog(self.grid_mode_selector.label)

    def option_selected(self, grid_mode: str):
        self.grid_mode_selector.set_current_grid_mode(grid_mode)
