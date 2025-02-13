from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTabFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        gen_tab = self.main_widget.generate_tab

        labels = [
            gen_tab.length_adjuster.length_label,
            gen_tab.length_adjuster.length_value_label,
            gen_tab.turn_intensity.intensity_label,
            gen_tab.turn_intensity.intensity_value_label,
            gen_tab.slice_size_toggle.halved_label,
            gen_tab.slice_size_toggle.quartered_label,
            gen_tab.permutation_type.mirrored_label,
            gen_tab.permutation_type.rotated_label,
        ]

        self._apply_font_colors(labels)
        gen_tab.prop_continuity_toggle.update_mode_label_styles()
        gen_tab.prop_continuity_toggle.update_mode_label_styles()
