# background_dialog.py
from typing import TYPE_CHECKING
from ..options_dialog import OptionsDialog

if TYPE_CHECKING:
    from .background_selector import BackgroundSelector


class BackgroundDialog:
    def __init__(self, background_selector: "BackgroundSelector"):
        self.background_selector = background_selector
        self.options = [
            "Rainbow",
            "Starfield",
            "Particle",
            "Aurora",
            "AuroraBorealis",
            "Snowfall",
            "Bubbles",
        ]

    def show_dialog(self):
        dialog = OptionsDialog(
            selector=self.background_selector,
            options=self.options,
            callback=self.option_selected,
        )
        dialog.show_dialog(self.background_selector.label)

    def option_selected(self, background: str):
        self.background_selector.set_current_background(background)
