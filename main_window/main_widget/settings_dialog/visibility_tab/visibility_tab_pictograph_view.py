from PyQt6.QtWidgets import QGraphicsItemGroup
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.pictograph_view import PictographView
from typing import TYPE_CHECKING

from base_widgets.base_pictograph.tka_glyph.base_glyph import BaseGlyph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import VisibilityTab


class VisibilityTabPictographView(PictographView):
    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.pictograph = self._initialize_example_pictograph()
        super().__init__(self.pictograph)
        self.set_clickable_glyphs()

    def _initialize_example_pictograph(self) -> BasePictograph:
        """Create and initialize the example pictograph."""
        example_data = {
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "blue_motion_type": "pro",
            "red_motion_type": "pro",
        }
        pictograph = BasePictograph(self.main_widget)
        pictograph_dict = self._find_pictograph_dict(example_data)
        pictograph.red_reversal = True
        pictograph.blue_reversal = True
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph

    def _find_pictograph_dict(self, example_data: dict) -> dict:
        """Find and return the appropriate pictograph dictionary."""
        from Enums.letters import Letter
        from copy import deepcopy

        target_letter = next(
            (l for l in Letter if l.value == example_data["letter"]), None
        )
        if not target_letter:
            print(
                f"Warning: Letter '{example_data['letter']}' not found in Letter Enum."
            )
            return {}

        letter_dicts = self.main_widget.pictograph_dicts.get(target_letter, [])
        for pdict in letter_dicts:
            if (
                pdict.get("start_pos") == example_data["start_pos"]
                and pdict.get("end_pos") == example_data["end_pos"]
                and pdict.get("blue_attributes", {}).get("motion_type")
                == example_data["blue_motion_type"]
                and pdict.get("red_attributes", {}).get("motion_type")
                == example_data["red_motion_type"]
            ):
                return deepcopy(pdict)
        return {}

    def update_visibility_from_settings(self):
        """Update glyph visibility based on settings."""
        for glyph in self._get_all_glyphs():
            visibility_manager = (
                self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
            )
            glyph.setVisible(visibility_manager.should_glyph_be_visible(glyph.name))

    def _get_all_glyphs(self) -> list[QGraphicsItemGroup]:
        """Return a list of all glyphs in the pictograph."""
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def set_clickable_glyphs(self):
        """Enable glyphs to be clickable and toggle visibility."""
        for glyph in self._get_all_glyphs():
            glyph.mousePressEvent = self._create_mouse_press_event(glyph)

    def _create_mouse_press_event(self, glyph):
        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)

        return mousePressEvent

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle glyph visibility and synchronize with checkboxes."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        manager = settings.glyph_visibility_manager
        current_visibility = manager.should_glyph_be_visible(glyph.name)
        settings.set_glyph_visibility(glyph.name, not current_visibility)
        self.visibility_tab.checkbox_widget.update_checkboxes()
