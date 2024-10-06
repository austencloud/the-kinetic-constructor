# visibility_dialog.py
from typing import TYPE_CHECKING
from ..checkbox_dialog import CheckboxDialog

if TYPE_CHECKING:
    from .visibility_selector import VisibilitySelector


class VisibilityDialog:
    def __init__(self, visibility_selector: "VisibilitySelector"):
        self.visibility_selector = visibility_selector
        self.glyph_visibility_manager = (
            visibility_selector.settings_manager.visibility.glyph_visibility_manager
        )
        self.grid_visibility_manager = (
            visibility_selector.settings_manager.visibility.grid_visibility_manager
        )

    def show_dialog(self):
        glyph_types = ["TKA", "VTG", "Elemental", "EndPosition"]
        options = {
            f"{glyph} Glyph": self.glyph_visibility_manager.get_glyph_visibility(glyph)
            for glyph in glyph_types
        }
        options["Non-Radial Points"] = self.grid_visibility_manager.non_radial_visible

        dialog = CheckboxDialog(
            parent=self.visibility_selector,
            options=options,
            callback=self.option_toggled,
        )
        dialog.show_dialog(self.visibility_selector.button)

    def option_toggled(self, option: str, visible: bool):
        if option == "Non-Radial Points":
            self.grid_visibility_manager.set_non_radial_visibility(visible)
        elif option.endswith(" Glyph"):
            glyph = option[:-6]  # Remove ' Glyph'
            self.glyph_visibility_manager.set_glyph_visibility(glyph, visible)
